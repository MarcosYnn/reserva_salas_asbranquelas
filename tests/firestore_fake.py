"""Armazenamento MVCC para testar a lógica com o decorator real do SDK.

Não substitui a homologação no Firestore: simula snapshots, conflitos de
versão e rollback, sem credenciais nem operações externas.
"""

from copy import deepcopy
from threading import RLock
from uuid import uuid4

from google.api_core.exceptions import Aborted


class Snapshot:
    def __init__(self, path, data):
        self.id = path.rsplit("/", 1)[-1]
        self.exists = data is not None
        self.data = deepcopy(data)

    def to_dict(self):
        return deepcopy(self.data)


class Reference:
    def __init__(self, db, path):
        self.db, self.path = db, path
        self.id = path.rsplit("/", 1)[-1]

    def get(self, transaction=None):
        if transaction:
            return transaction.read(self.path)
        with self.db.lock:
            return Snapshot(self.path, self.db.data.get(self.path))

    def collection(self, name):
        return Query(self.db, self.path + "/" + name)

    def set(self, data):
        with self.db.lock:
            self.db.write(self.path, data)

    def delete(self):
        with self.db.lock:
            self.db.write(self.path, None)


class Query:
    def __init__(self, db, path, filters=()):
        self.db, self.path, self.filters = db, path, filters

    def document(self, key=None):
        return Reference(self.db, self.path + "/" + (str(key) if key is not None else uuid4().hex))

    def where(self, *, filter):
        assert filter.op_string == "=="
        return Query(self.db, self.path, self.filters + ((filter.field_path, filter.value),))

    def matches(self, path, data):
        return (
            path.rsplit("/", 1)[0] == self.path
            and all(data.get(field) == value for field, value in self.filters)
        )

    def stream(self):
        with self.db.lock:
            return iter([
                Snapshot(path, data) for path, data in self.db.data.items()
                if self.matches(path, data)
            ])


class Transaction:
    _read_only = False
    _max_attempts = 5

    def __init__(self, db):
        self.db = db
        self.attempt = 0

    def _clean_up(self):
        self._id = None

    def _begin(self, retry_id=None):
        with self.db.lock:
            self.snapshot = deepcopy(self.db.data)
            self.versions = dict(self.db.versions)
        self.attempt += 1
        self.reads = set()
        self.writes = []
        self._id = uuid4().bytes

    def read(self, path):
        assert not self.writes, "Uma leitura ocorreu depois de uma escrita."
        self.reads.add(path)
        return Snapshot(path, self.snapshot.get(path))

    def get(self, query):
        assert not self.writes, "Uma consulta ocorreu depois de uma escrita."
        result = []
        for path, data in self.snapshot.items():
            if query.matches(path, data):
                self.reads.add(path)
                result.append(Snapshot(path, data))
        return iter(result)

    def update(self, reference, data):
        assert reference.path in self.snapshot
        self.writes.append((reference.path, {**self.snapshot[reference.path], **data}))

    def set(self, reference, data):
        self.writes.append((reference.path, data))

    def delete(self, reference):
        self.writes.append((reference.path, None))

    def _commit(self):
        if self.db.barrier is not None and self.attempt == 1:
            self.db.barrier.wait(timeout=5)
        with self.db.lock:
            if any(self.db.versions.get(path, 0) != self.versions.get(path, 0)
                   for path in self.reads):
                self.db.aborts += 1
                raise Aborted("Snapshot alterado por outra transação.")
            for path, data in self.writes:
                self.db.write(path, data)

    def _rollback(self):
        self.writes = []


class FirestoreFake:
    def __init__(self, data=None):
        self.data = deepcopy(data or {})
        self.versions = {path: 1 for path in self.data}
        self.lock = RLock()
        self.barrier = None
        self.aborts = 0

    def collection(self, name):
        return Query(self, name)

    def transaction(self):
        return Transaction(self)

    def write(self, path, data):
        if data is None:
            self.data.pop(path, None)
        else:
            self.data[path] = deepcopy(data)
        self.versions[path] = self.versions.get(path, 0) + 1
