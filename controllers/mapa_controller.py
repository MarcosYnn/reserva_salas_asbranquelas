
import heapq
import math


# Coordenadas de referencia dos locais na imagem 1535 x 1024
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


# Rede de corredores e passagens do campus
CAMINHOS = {
    # Entrada principal e corredor inferior
    "entrada": (695, 825),
    "inferior_centro": (695, 790),
    "inferior_esquerda": (390, 790),
    "inferior_direita": (990, 790),

    # Passagem entre os anfiteatros
    "anf_centro_baixo": (695, 760),
    "anf_centro_cima": (695, 610),
    "anf_esquerda": (390, 610),
    "anf_direita": (990, 610),

    # Corredores da biblioteca
    "biblioteca_sul": (695, 610),
    "biblioteca_oeste": (535, 610),
    "biblioteca_leste": (785, 610),

    # Corredor dos laboratorios de informatica
    "oeste_sul": (325, 610),
    "oeste_meio": (325, 430),
    "oeste_norte": (325, 245),
    "oeste_extremo_sul": (75, 610),
    "oeste_extremo_norte": (75, 245),

    # Corredor dos blocos de aula
    "blocos_sul": (535, 550),
    "blocos_meio": (535, 380),
    "blocos_norte": (535, 245),

    # Praca Central e suas passagens
    "praca_oeste": (575, 380),
    "praca_centro": (675, 380),
    "praca_leste": (775, 380),
    "praca_norte": (675, 300),
    "praca_sul": (675, 455),

    # Passagem pela direita da Biblioteca
    "central_sul": (785, 610),
    "biblioteca_direita": (785, 550),
    "central_meio": (785, 450),

    # Entrada inferior direita da Praca Central
    "praca_entrada_direita": (775, 420),
    # Cantina e corredor direito
    "cantina_sul": (920, 425),
    "direita_meio": (1080, 425),
    "direita_norte": (1080, 245),
    "direita_sul": (1080, 635),
    "direita_inferior": (1080, 800),

    # Corredores das quadras
    "quadras_sul": (950, 635),
    "quadras_leste": (1090, 635),

    # Extremo direito
    "extremo_direito_norte": (1280, 245),
    "extremo_direito_meio": (1280, 430),
    "extremo_direito_sul": (1280, 610),

    # Corredor superior
    "superior_esquerda": (535, 245),
    "superior_centro": (780, 245),
    "superior_direita": (1080, 245),
}


# Conexoes entre pontos de circulacao
LIGACOES = [
    # Entrada
    ("entrada", "inferior_centro"),
    ("inferior_centro", "inferior_esquerda"),
    ("inferior_centro", "inferior_direita"),
    ("inferior_centro", "anf_centro_baixo"),

    # Corredor inferior e anfiteatros
    ("inferior_esquerda", "anf_esquerda"),
    ("inferior_direita", "direita_inferior"),
    ("anf_centro_baixo", "anf_centro_cima"),
    ("anf_centro_cima", "biblioteca_sul"),
    ("anf_esquerda", "biblioteca_oeste"),
    ("anf_direita", "quadras_sul"),

    # Biblioteca
    ("biblioteca_sul", "biblioteca_oeste"),
    ("biblioteca_sul", "biblioteca_leste"),
    ("biblioteca_leste", "central_sul"),
    # Caminho pela direita da Biblioteca
    ("central_sul", "biblioteca_direita"),
    ("biblioteca_direita", "central_meio"),

    # Acesso a Praca Central pela direita
    ("central_meio", "praca_entrada_direita"),
    ("praca_entrada_direita", "praca_leste"),

    # Corredor esquerdo
    ("anf_esquerda", "oeste_sul"),
    ("oeste_sul", "oeste_meio"),
    ("oeste_meio", "oeste_norte"),
    ("oeste_sul", "oeste_extremo_sul"),
    ("oeste_extremo_sul", "oeste_extremo_norte"),
    ("oeste_extremo_norte", "oeste_norte"),

    # Salas de aula
    ("oeste_norte", "blocos_norte"),
    ("oeste_meio", "blocos_meio"),
    ("oeste_sul", "blocos_sul"),
    ("blocos_norte", "blocos_meio"),
    ("blocos_meio", "blocos_sul"),
    ("blocos_sul", "biblioteca_oeste"),

    # Passagens pela Praca Central
    ("blocos_meio", "praca_oeste"),
    ("praca_oeste", "praca_centro"),
    ("praca_centro", "praca_leste"),
    ("praca_centro", "praca_norte"),
    ("praca_centro", "praca_sul"),
    ("praca_leste", "central_meio"),

    # Corredor superior
    ("blocos_norte", "superior_esquerda"),
    ("superior_esquerda", "superior_centro"),
    ("superior_centro", "superior_direita"),
    ("praca_norte", "superior_centro"),

    # Corredor da cantina
    ("central_meio", "cantina_sul"),
    ("cantina_sul", "direita_meio"),
    ("direita_meio", "direita_norte"),
    ("direita_norte", "superior_direita"),

    # Corredor direito
    ("direita_meio", "direita_sul"),
    ("direita_sul", "direita_inferior"),
    ("direita_sul", "quadras_leste"),
    ("quadras_leste", "quadras_sul"),
    ("quadras_sul", "central_sul"),

    # Extremo direito
    ("direita_norte", "extremo_direito_norte"),
    ("extremo_direito_norte", "extremo_direito_meio"),
    ("extremo_direito_meio", "extremo_direito_sul"),
    ("extremo_direito_meio", "direita_meio"),
    ("extremo_direito_sul", "direita_sul"),
]


# Entradas aproximadas dos edificios
PORTAS = {
    "Entrada Principal": (695, 870),
    "Recepcao e Informacoes": (310, 855),

    "Laboratorio de Informatica 1": (310, 275),
    "Laboratorio de Informatica 2": (310, 320),
    "Laboratorio de Informatica 3": (310, 365),
    "Laboratorio de Informatica 4": (310, 455),
    "Laboratorio de Informatica 5": (310, 500),
    "Laboratorio de Informatica 6": (310, 545),

    "Salas de Aula - Bloco A": (525, 285),
    "Salas de Aula - Bloco B": (525, 380),
    "Salas de Aula - Bloco C": (525, 475),

    "Biblioteca": (660, 600),
    "Auditorio": (1140, 795),
    "Anfiteatro 1": (560, 625),
    "Anfiteatro 2": (820, 625),
    "Espaco Maker": (345, 675),

    "Praca Central": (675, 380),
    "Cantina": (920, 385),
    "Piscina": (700, 245),

    "Quadra Poliesportiva 1": (860, 635),
    "Quadra Poliesportiva 2": (1000, 635),

    "Laboratorio de Engenharia Civil": (300, 245),
    "Laboratorio de Fisioterapia": (1060, 245),
    "Laboratorio de Odontologia": (1100, 345),
    "Laboratorio de Medicina": (1100, 475),
}


# Conexao entre cada entrada e o corredor mais adequado
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
    "Auditorio": "direita_inferior",
    "Anfiteatro 1": "anf_esquerda",
    "Anfiteatro 2": "anf_centro_cima",
    "Espaco Maker": "oeste_sul",

    "Praca Central": "praca_centro",
    "Cantina": "cantina_sul",
    "Piscina": "superior_centro",

    "Quadra Poliesportiva 1": "central_sul",
    "Quadra Poliesportiva 2": "quadras_sul",

    "Laboratorio de Engenharia Civil": "oeste_norte",
    "Laboratorio de Fisioterapia": "direita_norte",
    "Laboratorio de Odontologia": "direita_meio",
    "Laboratorio de Medicina": "direita_sul",
}


def distancia(ponto1, ponto2):
    return math.dist(ponto1, ponto2)


def calcular_rota(origem, destino):
    if origem not in LOCAIS or destino not in LOCAIS:
        return []

    if origem == destino:
        return [PORTAS[origem]]

    pontos = CAMINHOS.copy()
    pontos["origem"] = PORTAS[origem]
    pontos["destino"] = PORTAS[destino]

    grafo = {nome: [] for nome in pontos}

    for a, b in LIGACOES:
        if a not in pontos or b not in pontos:
            continue

        peso = distancia(pontos[a], pontos[b])

        grafo[a].append((b, peso))
        grafo[b].append((a, peso))

    # Conecta origem e destino aos seus acessos
    for nome, local in (
        ("origem", origem),
        ("destino", destino),
    ):
        acesso = ACESSOS.get(local)

        if acesso not in pontos:
            return []

        peso = distancia(pontos[nome], pontos[acesso])

        grafo[nome].append((acesso, peso))
        grafo[acesso].append((nome, peso))

    # Algoritmo de Dijkstra
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
                heapq.heappush(
                    fila,
                    (novo_custo, vizinho)
                )

    if "destino" not in menores:
        return []

    # Reconstrucao da rota
    rota = []
    atual = "destino"

    while atual != "origem":
        rota.append(pontos[atual])
        atual = anteriores[atual]

    rota.append(pontos["origem"])
    rota.reverse()

    return rota
