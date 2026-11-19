
import heapq
import math

LARGURA_MAPA = 1535
ALTURA_MAPA = 1024

# ==========================================
# LOCAIS DO CAMPUS
# ==========================================

LOCAIS = {
    'Entrada Principal': (698, 875),
    'Recepcao e Informacoes': (300, 805),
    **{
        f'Laboratorio de Informatica {i}': p
        for i, p in enumerate([
            (210, 275),
            (210, 320),
            (210, 365),
            (210, 455),
            (210, 500),
            (210, 545)
        ], 1)
    },
    'Salas de Aula - Bloco A': (435, 285),
    'Salas de Aula - Bloco B': (435, 380),
    'Salas de Aula - Bloco C': (435, 475),
    'Biblioteca': (660, 515),
    'Auditorio': (1145, 710),
    'Anfiteatro 1': (555, 690),
    'Anfiteatro 2': (845, 690),
    'Espaco Maker': (230, 675),
    'Praca Central': (670, 375),
    'Cantina': (920, 320),
    'Piscina': (690, 180),
    'Quadra Poliesportiva 1': (860, 545),
    'Quadra Poliesportiva 2': (1000, 545),
    'Laboratorio de Engenharia Civil': (300, 170),
    'Laboratorio de Fisioterapia': (1060, 170),
    'Laboratorio de Odontologia': (1170, 345),
    'Laboratorio de Medicina': (1190, 475),
}

# ==========================================
# VERTICES E CORREDORES
# ==========================================

CAMINHOS = {}
LIGACOES = []
_NOS_COORDENADAS = {}


def adicionar_ponto(coordenada):
    if coordenada not in _NOS_COORDENADAS:
        nome = f'ponto_{len(CAMINHOS) + 1}'
        CAMINHOS[nome] = coordenada
        _NOS_COORDENADAS[coordenada] = nome

    return _NOS_COORDENADAS[coordenada]


def adicionar_corredor(*coordenadas):
    pontos = [
        adicionar_ponto(p)
        for p in coordenadas
    ]

    for a, b in zip(pontos, pontos[1:]):
        if a != b:
            if (a, b) not in LIGACOES and (b, a) not in LIGACOES:
                LIGACOES.append((a, b))


# ==========================================
# CORREDOR SUPERIOR
# ==========================================

adicionar_corredor(
    (105, 253),
    (137, 253),
    (289, 253),
    (343, 256),
    (457, 253),
    (519, 246),
    (532, 253),
    (691, 253),
    (775, 253),
    (929, 253),
    (1059, 253),
    (1130, 253),
    (1225, 253)
)

# Engenharia Civil - acesso esquerdo

adicionar_corredor(
    (137, 253),
    (141, 186),
    (145, 143)
)

# Engenharia Civil - acesso direito

adicionar_corredor(
    (457, 253),
    (460, 186),
    (460, 145)
)

# Corredor superior auxiliar

adicionar_corredor(
    (519, 246),
    (519, 140)
)

# Fisioterapia

adicionar_corredor(
    (929, 253),
    (925, 179),
    (919, 137)
)

# ==========================================
# LABORATORIOS DE INFORMATICA
# ==========================================

# Corredor externo dos laboratorios 1, 2 e 3

adicionar_corredor(
    (105, 253),
    (98, 285),
    (96, 325),
    (92, 367),
    (86, 410),
    (105, 430)
)

# Passagem autorizada entre os laboratorios 3 e 4

adicionar_corredor(
    (105, 430),
    (223, 430),
    (340, 435)
)

# Corredor externo dos laboratorios 4, 5 e 6

adicionar_corredor(
    (105, 430),
    (85, 474),
    (78, 509),
    (74, 563),
    (72, 592),
    (97, 621),
    (121, 627)
)

# Corredor inferior dos laboratorios

adicionar_corredor(
    (121, 627),
    (200, 627),
    (373, 627),
    (397, 627),
    (434, 627)
)

# Corredor entre laboratorios e blocos de aula

adicionar_corredor(
    (343, 256),
    (340, 343),
    (340, 435),
    (338, 549),
    (375, 553),
    (373, 627)
)

# ==========================================
# BLOCOS DE SALAS DE AULA
# ==========================================

# Passagem entre blocos A e B

adicionar_corredor(
    (340, 343),
    (445, 343),
    (531, 343)
)

# Passagem entre blocos B e C

adicionar_corredor(
    (340, 435),
    (441, 435),
    (530, 436)
)

# Corredor lateral direito dos blocos

adicionar_corredor(
    (532, 253),
    (531, 343),
    (534, 376),
    (530, 436),
    (535, 471),
    (530, 535),
    (495, 535),
    (436, 535)
)

# ==========================================
# PRACA CENTRAL
# ==========================================

adicionar_corredor(
    (534, 376),
    (567, 376)
)

adicionar_corredor(
    (535, 471),
    (661, 471),
    (788, 471)
)

# Acesso sul da praca

adicionar_corredor(
    (661, 471),
    (661, 433)
)

# Corredor entre praca e cantina

adicionar_corredor(
    (775, 253),
    (775, 360),
    (776, 413),
    (790, 428),
    (788, 461),
    (788, 471)
)

# ==========================================
# CANTINA E FUNDOS DOS LABORATORIOS
# ==========================================

adicionar_corredor(
    (790, 428),
    (829, 428),
    (1017, 424),
    (1083, 421),
    (1188, 421)
)

adicionar_corredor(
    (1059, 253),
    (1083, 421),
    (1097, 461)
)

# ==========================================
# BIBLIOTECA E JARDINS
# ==========================================

adicionar_corredor(
    (436, 535),
    (436, 582),
    (434, 627)
)

adicionar_corredor(
    (436, 535),
    (495, 535),
    (533, 587)
)

adicionar_corredor(
    (434, 627),
    (533, 587),
    (559, 587),
    (595, 609),
    (660, 609),
    (725, 609),
    (789, 580)
)

adicionar_corredor(
    (434, 627),
    (595, 627),
    (660, 629),
    (698, 629),
    (790, 629)
)

adicionar_corredor(
    (595, 609),
    (595, 627)
)

adicionar_corredor(
    (660, 609),
    (660, 629)
)

adicionar_corredor(
    (788, 471),
    (789, 580),
    (790, 629)
)

# ==========================================
# QUADRAS POLIESPORTIVAS
# ==========================================

adicionar_corredor(
    (788, 461),
    (927, 461),
    (1097, 461)
)

adicionar_corredor(
    (927, 461),
    (927, 485),
    (935, 601),
    (935, 629)
)

adicionar_corredor(
    (790, 629),
    (935, 629),
    (971, 629),
    (1105, 629)
)

# ==========================================
# ODONTOLOGIA E MEDICINA
# ==========================================

adicionar_corredor(
    (1097, 461),
    (1119, 578),
    (1105, 629)
)

adicionar_corredor(
    (1119, 578),
    (1200, 578)
)

# ==========================================
# ESPACO MAKER E RECEPCAO
# ==========================================

adicionar_corredor(
    (121, 627),
    (106, 724),
    (216, 726),
    (393, 724)
)

adicionar_corredor(
    (397, 627),
    (393, 724),
    (388, 753)
)

adicionar_corredor(
    (216, 726),
    (215, 753),
    (388, 753)
)

adicionar_corredor(
    (393, 724),
    (465, 803),
    (480, 805)
)

adicionar_corredor(
    (465, 803),
    (458, 859),
    (309, 859)
)

# ==========================================
# ANFITEATROS E AUDITORIO
# ==========================================

# Corredor inferior

adicionar_corredor(
    (480, 805),
    (557, 806),
    (698, 806),
    (846, 806),
    (983, 806),
    (1147, 806)
)

# Corredor entre anfiteatros

adicionar_corredor(
    (698, 629),
    (698, 707),
    (698, 806)
)

# Corredor entre anfiteatro 2 e auditorio

adicionar_corredor(
    (971, 629),
    (977, 707),
    (983, 806)
)

# Entrada principal

adicionar_corredor(
    (698, 806),
    (698, 838),
    (698, 875)
)

# ==========================================
# PORTAS E ACESSOS
# ==========================================

# Porta azul e ponto amarelo correspondente.

DADOS_ACESSOS = {
    'Entrada Principal': (
        (698, 875), (698, 875)
    ),
    'Recepcao e Informacoes': (
        (309, 844), (309, 859)
    ),
    'Laboratorio de Informatica 1': (
        (110, 285), (98, 285)
    ),
    'Laboratorio de Informatica 2': (
        (106, 325), (96, 325)
    ),
    'Laboratorio de Informatica 3': (
        (102, 367), (92, 367)
    ),
    'Laboratorio de Informatica 4': (
        (99, 474), (85, 474)
    ),
    'Laboratorio de Informatica 5': (
        (94, 509), (78, 509)
    ),
    'Laboratorio de Informatica 6': (
        (88, 563), (74, 563)
    ),
    'Salas de Aula - Bloco A': (
        (445, 343), (445, 343)
    ),
    'Salas de Aula - Bloco B': (
        (441, 422), (441, 435)
    ),
    'Salas de Aula - Bloco C': (
        (436, 521), (436, 535)
    ),
    'Biblioteca': (
        (660, 595), (660, 609)
    ),
    'Auditorio': (
        (1147, 787), (1147, 806)
    ),
    'Anfiteatro 1': (
        (557, 788), (557, 806)
    ),
    'Anfiteatro 2': (
        (846, 788), (846, 806)
    ),
    'Espaco Maker': (
        (216, 712), (216, 726)
    ),
    'Praca Central': (
        (567, 376), (534, 376)
    ),
    'Cantina': (
        (1017, 407), (1017, 424)
    ),
    'Piscina': (
        (691, 232), (691, 253)
    ),
    'Quadra Poliesportiva 1': (
        (935, 601), (935, 601)
    ),
    'Quadra Poliesportiva 2': (
        (927, 485), (927, 485)
    ),
    'Laboratorio de Engenharia Civil': (
        (155, 186), (141, 186)
    ),
    'Laboratorio de Fisioterapia': (
        (938, 179), (925, 179)
    ),
    'Laboratorio de Odontologia': (
        (1131, 270), (1130, 253)
    ),
    'Laboratorio de Medicina': (
        (1197, 540), (1200, 578)
    ),
}

PORTAS = {
    local: dados[0]
    for local, dados in DADOS_ACESSOS.items()
}

ACESSOS = {
    local: _NOS_COORDENADAS[dados[1]]
    for local, dados in DADOS_ACESSOS.items()
}

# ==========================================
# CALCULO DE DISTANCIA
# ==========================================

def distancia(ponto1, ponto2):
    return math.hypot(
        ponto2[0] - ponto1[0],
        ponto2[1] - ponto1[1]
    )


# ==========================================
# VALIDACAO DO GRAFO
# ==========================================

def validar_grafo():
    problemas = []

    for a, b in LIGACOES:
        if a not in CAMINHOS:
            problemas.append(f'Ponto inexistente: {a}')

        if b not in CAMINHOS:
            problemas.append(f'Ponto inexistente: {b}')

    for local in LOCAIS:
        if local not in PORTAS:
            problemas.append(f'Porta ausente: {local}')

        if ACESSOS.get(local) not in CAMINHOS:
            problemas.append(f'Acesso invalido: {local}')

    for nome, (x, y) in CAMINHOS.items():
        if not (0 <= x < LARGURA_MAPA and
                0 <= y < ALTURA_MAPA):
            problemas.append(f'Ponto fora do mapa: {nome}')

    if problemas:
        return problemas

    for local in LOCAIS:
        if not calcular_rota('Entrada Principal', local):
            problemas.append(f'Local sem rota: {local}')

    return problemas


# ==========================================
# ALGORITMO DE DIJKSTRA
# ==========================================

def calcular_rota(origem, destino):

    if origem not in LOCAIS or destino not in LOCAIS:
        return []

    if origem == destino:
        return [PORTAS[origem]]

    pontos = CAMINHOS.copy()

    pontos['origem'] = PORTAS[origem]
    pontos['destino'] = PORTAS[destino]

    grafo = {
        nome: []
        for nome in pontos
    }

    for a, b in LIGACOES:

        if a not in pontos or b not in pontos:
            continue

        peso = distancia(pontos[a], pontos[b])

        grafo[a].append((b, peso))
        grafo[b].append((a, peso))

    for nome, local in (
        ('origem', origem),
        ('destino', destino)
    ):

        acesso = ACESSOS.get(local)

        if acesso not in pontos:
            return []

        peso = distancia(
            pontos[nome],
            pontos[acesso]
        )

        grafo[nome].append((acesso, peso))
        grafo[acesso].append((nome, peso))

    fila = [(0, 'origem')]
    menores = {'origem': 0}
    anteriores = {}

    while fila:

        custo, atual = heapq.heappop(fila)

        if custo > menores.get(atual, float('inf')):
            continue

        if atual == 'destino':
            break

        for vizinho, peso in grafo[atual]:

            novo_custo = custo + peso

            if novo_custo < menores.get(
                vizinho, float('inf')
            ):

                menores[vizinho] = novo_custo
                anteriores[vizinho] = atual

                heapq.heappush(
                    fila,
                    (novo_custo, vizinho)
                )

    if 'destino' not in menores:
        return []

    rota = []
    atual = 'destino'

    while atual != 'origem':

        rota.append(pontos[atual])
        atual = anteriores[atual]

    rota.append(pontos['origem'])
    rota.reverse()

    # Remove coordenadas consecutivas duplicadas.

    rota_final = []

    for ponto in rota:
        if not rota_final or rota_final[-1] != ponto:
            rota_final.append(ponto)

    return rota_final
def gerar_movimentacao(rota, passo=5):

    if not rota:
        return []

    posicoes = [rota[0]]

    for inicio, fim in zip(rota, rota[1:]):

        comprimento = distancia(inicio, fim)

        etapas = max(
            1, math.ceil(comprimento / passo)
        )

        for i in range(1, etapas + 1):

            t = i / etapas

            x = inicio[0] + (fim[0] - inicio[0]) * t
            y = inicio[1] + (fim[1] - inicio[1]) * t

            posicoes.append((round(x), round(y)))

    return posicoes