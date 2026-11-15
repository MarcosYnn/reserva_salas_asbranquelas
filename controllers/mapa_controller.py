
import heapq
import math


# Posicoes aproximadas dos locais na imagem (1535 x 1024)
LOCAIS = {
    "Entrada Principal": (695, 870),
    "Recepcao e Informacoes": (310, 800),
    "Laboratorio de Informatica 1": (210, 275),
    "Laboratorio de Informatica 2": (210, 320),
    "Laboratorio de Informatica 3": (210, 365),
    "Laboratorio de Informatica 4": (210, 455),
    "Laboratorio de Informatica 5": (210, 500),
    "Laboratorio de Informatica 6": (210, 545),
    "Salas de Aula - Bloco A": (430, 285),
    "Salas de Aula - Bloco B": (430, 380),
    "Salas de Aula - Bloco C": (430, 475),
    "Biblioteca": (660, 515),
    "Auditorio": (1140, 710),
    "Anfiteatro 1": (560, 690),
    "Anfiteatro 2": (820, 690),
    "Espaco Maker": (230, 675),
    "Praca Central": (675, 380),
    "Cantina": (920, 320),
    "Piscina": (700, 180),
    "Quadra Poliesportiva 1": (860, 545),
    "Quadra Poliesportiva 2": (1000, 545),
    "Laboratorio de Engenharia Civil": (300, 170),
    "Laboratorio de Fisioterapia": (1060, 170),
    "Laboratorio de Odontologia": (1170, 345),
    "Laboratorio de Medicina": (1190, 475),
}


# Pontos de circulacao estimados a partir do mapa ilustrado.
# As ligacoes precisam ser validadas no campus.
CAMINHOS = {
    # Corredor inferior
    "entrada": (695, 825),
    "inferior_centro": (695, 790),
    "inferior_esquerda": (390, 790),
    "inferior_direita": (990, 790),

    # Area dos anfiteatros
    "anf_esquerda": (450, 590),
    "anf_centro": (695, 590),
    "anf_direita": (970, 590),

    # Area da biblioteca e das quadras
    "biblioteca_sul": (660, 590),
    "biblioteca_oeste": (535, 570),
    "biblioteca_leste": (780, 570),
    "quadras_sul": (950, 630),
    "quadras_leste": (1090, 550),

    # Corredor esquerdo
    "oeste_sul": (350, 620),
    "oeste_meio": (325, 430),
    "oeste_norte": (325, 245),
    "oeste_extremo": (80, 620),
    "oeste_extremo_norte": (80, 245),

    # Corredor entre blocos e praca
    "blocos_sul": (535, 550),
    "blocos_meio": (535, 380),
    "blocos_norte": (535, 245),
    "praca_sul": (675, 465),
    "praca_norte": (675, 300),

    # Corredor central e direito
    "centro_leste": (780, 465),
    "cantina_sul": (920, 420),
    "direita_meio": (1080, 430),
    "direita_norte": (1080, 245),
    "direita_sul": (1080, 620),
    "extremo_direito": (1280, 430),
    "extremo_direito_sul": (1280, 620),

    # Circulacao superior
    "superior_esquerda": (535, 245),
    "superior_centro": (780, 245),
    "superior_direita": (1080, 245),
}


# Conexoes de circulacao inicialmente estimadas
LIGACOES = [
    ("entrada", "inferior_centro"),
    ("inferior_centro", "inferior_esquerda"),
    ("inferior_centro", "inferior_direita"),

    ("inferior_esquerda", "anf_esquerda"),
    ("inferior_centro", "anf_centro"),
    ("inferior_direita", "anf_direita"),

    ("anf_esquerda", "anf_centro"),
    ("anf_centro", "anf_direita"),

    ("anf_esquerda", "oeste_sul"),
    ("anf_centro", "biblioteca_sul"),
    ("anf_direita", "quadras_sul"),

    ("biblioteca_sul", "biblioteca_oeste"),
    ("biblioteca_sul", "biblioteca_leste"),
    ("biblioteca_oeste", "oeste_sul"),
    ("biblioteca_leste", "quadras_sul"),

    ("oeste_sul", "oeste_meio"),
    ("oeste_meio", "oeste_norte"),
    ("oeste_sul", "oeste_extremo"),
    ("oeste_extremo", "oeste_extremo_norte"),
    ("oeste_extremo_norte", "oeste_norte"),

    ("oeste_norte", "blocos_norte"),
    ("oeste_meio", "blocos_meio"),
    ("oeste_sul", "blocos_sul"),
    ("blocos_norte", "blocos_meio"),
    ("blocos_meio", "blocos_sul"),

    ("blocos_norte", "superior_esquerda"),
    ("superior_esquerda", "superior_centro"),
    ("superior_centro", "superior_direita"),

    ("blocos_meio", "praca_norte"),
    ("praca_norte", "praca_sul"),
    ("praca_sul", "centro_leste"),

    ("centro_leste", "cantina_sul"),
    ("cantina_sul", "direita_meio"),
    ("direita_meio", "direita_norte"),
    ("direita_meio", "direita_sul"),

    ("direita_norte", "superior_direita"),
    ("direita_meio", "extremo_direito"),
    ("extremo_direito", "extremo_direito_sul"),
    ("extremo_direito_sul", "direita_sul"),

    ("direita_sul", "quadras_leste"),
    ("quadras_leste", "quadras_sul"),
    ("quadras_sul", "anf_direita"),
]


# Cada local se conecta a um acesso definido.
ACESSOS = {
    "Entrada Principal": "entrada",
    "Recepcao e Informacoes": "inferior_esquerda",

    "Laboratorio de Informatica 1": "oeste_norte",
    "Laboratorio de Informatica 2": "oeste_norte",
    "Laboratorio de Informatica 3": "oeste_meio",
    "Laboratorio de Informatica 4": "oeste_meio",
    "Laboratorio de Informatica 5": "oeste_meio",
    "Laboratorio de Informatica 6": "oeste_sul",

    "Salas de Aula - Bloco A": "blocos_norte",
    "Salas de Aula - Bloco B": "blocos_meio",
    "Salas de Aula - Bloco C": "blocos_sul",

    "Biblioteca": "biblioteca_sul",
    "Auditorio": "inferior_direita",
    "Anfiteatro 1": "anf_esquerda",
    "Anfiteatro 2": "anf_direita",
    "Espaco Maker": "oeste_sul",

    "Praca Central": "praca_sul",
    "Cantina": "cantina_sul",
    "Piscina": "superior_centro",

    "Quadra Poliesportiva 1": "quadras_sul",
    "Quadra Poliesportiva 2": "quadras_sul",

    "Laboratorio de Engenharia Civil": "oeste_norte",
    "Laboratorio de Fisioterapia": "direita_norte",
    "Laboratorio de Odontologia": "extremo_direito",
    "Laboratorio de Medicina": "extremo_direito_sul",
}


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

    # Liga a origem e o destino aos acessos cadastrados
    for nome, local in (
        ("origem", origem),
        ("destino", destino)
    ):
        acesso = ACESSOS[local]
        peso = distancia(pontos[nome], pontos[acesso])

        grafo[nome].append((acesso, peso))
        grafo[acesso].append((nome, peso))

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
