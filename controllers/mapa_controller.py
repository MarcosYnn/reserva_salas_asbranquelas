
import heapq
import math


# Posicoes aproximadas dos locais na imagem (1535 x 1024)
LOCAIS = {
    "Entrada Principal": (695, 870),
    "Recepcao e Informacoes": (310, 860),
    "Laboratorio de Informatica 1": (210, 245),
    "Laboratorio de Informatica 2": (210, 300),
    "Laboratorio de Informatica 3": (210, 345),
    "Laboratorio de Informatica 4": (210, 430),
    "Laboratorio de Informatica 5": (210, 475),
    "Laboratorio de Informatica 6": (210, 580),
    "Salas de Aula - Bloco A": (430, 245),
    "Salas de Aula - Bloco B": (430, 345),
    "Salas de Aula - Bloco C": (430, 450),
    "Biblioteca": (660, 600),
    "Auditorio": (1130, 795),
    "Anfiteatro 1": (560, 735),
    "Anfiteatro 2": (820, 735),
    "Espaco Maker": (230, 730),
    "Praca Central": (675, 430),
    "Cantina": (910, 430),
    "Piscina": (700, 245),
    "Quadra Poliesportiva 1": (860, 630),
    "Quadra Poliesportiva 2": (1000, 630),
    "Laboratorio de Engenharia Civil": (300, 245),
    "Laboratorio de Fisioterapia": (1060, 245),
    "Laboratorio de Odontologia": (1170, 430),
    "Laboratorio de Medicina": (1190, 630),
}

# Pontos de passagem aproximados.
# Eles representam uma primeira rede de circulacao.
CAMINHOS = {
    "A": (80, 245),
    "B": (330, 245),
    "C": (535, 245),
    "D": (780, 245),
    "E": (1080, 245),
    "F": (1280, 245),

    "G": (80, 430),
    "H": (330, 430),
    "I": (535, 430),
    "J": (780, 430),
    "K": (1080, 430),
    "L": (1280, 430),

    "M": (80, 620),
    "N": (330, 620),
    "O": (535, 620),
    "P": (780, 620),
    "Q": (1080, 620),
    "R": (1280, 620),

    "S": (80, 750),
    "T": (330, 750),
    "U": (535, 750),
    "V": (780, 750),
    "W": (1080, 750),
    "X": (1280, 750),

    "Y": (695, 870),
    "Z": (695, 750),
}

# Ligacoes entre os pontos de passagem
LIGACOES = [
    ("A", "B"), ("B", "C"), ("C", "D"),
    ("D", "E"), ("E", "F"),

    ("G", "H"), ("H", "I"), ("I", "J"),
    ("J", "K"), ("K", "L"),

    ("M", "N"), ("N", "O"), ("O", "P"),
    ("P", "Q"), ("Q", "R"),

    ("S", "T"), ("T", "U"), ("U", "V"),
    ("V", "W"), ("W", "X"),

    ("A", "G"), ("G", "M"), ("M", "S"),
    ("B", "H"), ("H", "N"), ("N", "T"),
    ("C", "I"), ("I", "O"), ("O", "U"),
    ("D", "J"), ("J", "P"), ("P", "V"),
    ("E", "K"), ("K", "Q"), ("Q", "W"),
    ("F", "L"), ("L", "R"), ("R", "X"),

    ("Y", "Z"), ("Z", "V"),
]


def distancia(ponto1, ponto2):
    return math.dist(ponto1, ponto2)


def calcular_rota(origem, destino):
    if origem not in LOCAIS or destino not in LOCAIS:
        return []

    if origem == destino:
        return [LOCAIS[origem]]

    pontos = CAMINHOS.copy()
    pontos["origem"] = LOCAIS[origem]
    pontos["destino"] = LOCAIS[destino]

    grafo = {nome: [] for nome in pontos}

    for a, b in LIGACOES:
        peso = distancia(pontos[a], pontos[b])
        grafo[a].append((b, peso))
        grafo[b].append((a, peso))

    # Conecta os locais aos pontos de passagem mais proximos.
    # Estas conexoes devem ser revisadas com os acessos reais.
    for nome in ("origem", "destino"):
        proximos = sorted(
            CAMINHOS,
            key=lambda p: distancia(pontos[nome], pontos[p])
        )[:2]

        for ponto in proximos:
            peso = distancia(pontos[nome], pontos[ponto])
            grafo[nome].append((ponto, peso))
            grafo[ponto].append((nome, peso))

    fila = [(0, "origem")]
    menores = {"origem": 0}
    anteriores = {}

    while fila:
        custo, atual = heapq.heappop(fila)

        if custo > menores.get(atual, float("inf")):
            continue

        if atual == "destino":
            break

        for vizinho, peso in grafo[atual]:
            novo_custo = custo + peso

            if novo_custo < menores.get(vizinho, float("inf")):
                menores[vizinho] = novo_custo
                anteriores[vizinho] = atual
                heapq.heappush(fila, (novo_custo, vizinho))

    if "destino" not in anteriores:
        return []

    rota = []
    atual = "destino"

    while atual != "origem":
        rota.append(pontos[atual])
        atual = anteriores[atual]

    rota.append(pontos["origem"])
    rota.reverse()

    return rota
