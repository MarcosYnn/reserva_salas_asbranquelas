"""Regressão da validação de datas, sem operações no Firestore."""

import unittest
from datetime import datetime
from unittest.mock import patch

from models import reserva_firebase_model as model


class RelogioFixo(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2030, 5, 10, 12, 0, 30)


class ValidacaoDataHorariosTests(unittest.TestCase):
    def setUp(self):
        relogio = patch.object(model, "datetime", RelogioFixo)
        relogio.start()
        self.addCleanup(relogio.stop)

    def test_rejeita_data_passada(self):
        with self.assertRaisesRegex(ValueError, "data passada"):
            model._validar_data_horarios("2030-05-09", "14:00", "15:00")

    def test_rejeita_inicio_passado_hoje(self):
        with self.assertRaisesRegex(ValueError, "posterior ao horário atual"):
            model._validar_data_horarios("2030-05-10", "11:00", "13:00")

    def test_rejeita_minuto_que_ja_comecou(self):
        with self.assertRaisesRegex(ValueError, "posterior ao horário atual"):
            model._validar_data_horarios("2030-05-10", "12:00", "13:00")

    def test_aceita_inicio_futuro_hoje(self):
        self.assertIsNone(
            model._validar_data_horarios("2030-05-10", "12:01", "13:00")
        )

    def test_aceita_dia_futuro_com_hora_menor_que_agora(self):
        self.assertIsNone(
            model._validar_data_horarios("2030-05-11", "08:00", "09:00")
        )

    def test_rejeita_fim_anterior_ao_inicio(self):
        with self.assertRaisesRegex(ValueError, "depois do inicial"):
            model._validar_data_horarios("2030-05-11", "12:00", "11:00")

    def test_rejeita_inicio_e_fim_iguais(self):
        with self.assertRaisesRegex(ValueError, "depois do inicial"):
            model._validar_data_horarios("2030-05-11", "12:00", "12:00")

    def test_preserva_validacao_de_data_invalida(self):
        for data in ("2030-02-30", "10/05/2030", None):
            with self.subTest(data=data):
                with self.assertRaisesRegex(ValueError, "AAAA-MM-DD"):
                    model._validar_data_horarios(data, "14:00", "15:00")

    def test_preserva_validacao_de_hora_invalida(self):
        for inicio, fim in (("25:00", "15:00"), ("14:00", "25:00"), (None, "15:00")):
            with self.subTest(inicio=inicio, fim=fim):
                with self.assertRaisesRegex(ValueError, "HH:MM"):
                    model._validar_data_horarios("2030-05-11", inicio, fim)


if __name__ == "__main__":
    unittest.main()
