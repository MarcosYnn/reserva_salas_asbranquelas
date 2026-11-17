import heapq
import math

# Coordenadas aproximadas na imagem-base de 1535 x 1024 pixels.
LOCAIS = {
    'Entrada Principal': (695, 870),
    'Recepcao e Informacoes': (310, 800),
    **{f'Laboratorio de Informatica {i}': p for i,p in enumerate([(210,275),(210,320),(210,365),(210,455),(210,500),(210,545)],1)},
    'Salas de Aula - Bloco A': (430,285),
    'Salas de Aula - Bloco B': (430,380),
    'Salas de Aula - Bloco C': (430,475),
    'Biblioteca': (660,515), 'Auditorio': (1140,710),
    'Anfiteatro 1': (560,690), 'Anfiteatro 2': (820,690),
    'Espaco Maker': (230,675), 'Praca Central': (675,380),
    'Cantina': (920,320), 'Piscina': (700,180),
    'Quadra Poliesportiva 1': (860,545),
    'Quadra Poliesportiva 2': (1000,545),
    'Laboratorio de Engenharia Civil': (300,170),
    'Laboratorio de Fisioterapia': (1060,170),
    'Laboratorio de Odontologia': (1170,345),
    'Laboratorio de Medicina': (1190,475),
}

CAMINHOS = {
    'entrada': (695,825), 'inferior_centro': (695,790),
    'inferior_esquerda': (390,790), 'inferior_direita': (990,790),
    'anf_centro_baixo': (695,760), 'anf_centro_cima': (695,610),
    'anf_esquerda': (390,610), 'anf_direita': (990,610),
    'biblioteca_sul': (695,610), 'biblioteca_oeste': (535,610),
    'biblioteca_oeste_meio': (535,570), 'biblioteca_leste': (785,610),
    'biblioteca_direita': (785,550),
    'oeste_sul': (325,610), 'oeste_meio': (325,430),
    'oeste_norte': (325,245),
    'lab_1_acesso': (325,275), 'lab_2_acesso': (325,320),
    'lab_3_acesso': (325,365), 'lab_4_acesso': (325,455),
    'lab_5_acesso': (325,500), 'lab_6_acesso': (325,545),
    # Travessia publica confirmada entre os laboratorios 3 e 4.
    'travessia_lab_3_4': (325,415),
    'oeste_extremo_sul': (75,610), 'oeste_extremo_norte': (75,245),
    'blocos_sul': (535,550), 'blocos_meio': (535,380),
    'blocos_norte': (535,245),
    'praca_oeste': (575,380), 'praca_centro': (675,380),
    'praca_leste': (775,380), 'praca_norte': (675,300),
    'praca_sul': (675,455), 'praca_entrada_direita': (775,420),
    'central_sul': (785,610), 'central_meio': (785,450),
    'cantina_sul': (920,425), 'direita_meio': (1080,425),
    'direita_norte': (1080,245), 'direita_sul': (1080,635),
    'direita_inferior': (1080,800), 'quadras_sul': (950,635),
    'quadras_leste': (1090,635),
    'extremo_direito_norte': (1280,245),
    'extremo_direito_meio': (1280,430),
    'extremo_direito_sul': (1280,610),
    'superior_esquerda': (535,245),
    'superior_centro': (780,245),
    'superior_direita': (1080,245),
    # Passagens entre os blocos de aula (pontos para inspeção visual).
    'passagem_bloco_a_b': (535,335),
    'passagem_bloco_b_c': (535,430),
}

LIGACOES = [
    ('entrada','inferior_centro'),
    ('inferior_centro','inferior_esquerda'),
    ('inferior_centro','inferior_direita'),
    ('inferior_centro','anf_centro_baixo'),
    ('inferior_esquerda','anf_esquerda'),
    ('inferior_direita','direita_inferior'),
    ('anf_centro_baixo','anf_centro_cima'),
    ('anf_centro_cima','biblioteca_sul'),
    ('anf_esquerda','biblioteca_oeste'),
    ('anf_direita','quadras_sul'),
    ('biblioteca_sul','biblioteca_oeste'),
    ('biblioteca_sul','biblioteca_leste'),
    ('biblioteca_leste','central_sul'),
    ('central_sul','biblioteca_direita'),
    ('biblioteca_direita','central_meio'),
    ('central_meio','praca_entrada_direita'),
    ('praca_entrada_direita','praca_leste'),
    ('anf_esquerda','oeste_sul'),
    ('oeste_sul','lab_6_acesso'),
    ('lab_6_acesso','lab_5_acesso'),
    ('lab_5_acesso','lab_4_acesso'),
    ('lab_4_acesso','oeste_meio'),
    ('oeste_meio','travessia_lab_3_4'),
    ('travessia_lab_3_4','lab_3_acesso'),
    ('lab_3_acesso','lab_2_acesso'),
    ('lab_2_acesso','lab_1_acesso'),
    ('lab_1_acesso','oeste_norte'),
    ('oeste_sul','oeste_extremo_sul'),
    ('oeste_extremo_sul','oeste_extremo_norte'),
    ('oeste_extremo_norte','oeste_norte'),
    ('oeste_norte','blocos_norte'),
    # As passagens entre blocos seguem o corredor vertical lateral.
    ('blocos_norte','passagem_bloco_a_b'),
    ('passagem_bloco_a_b','blocos_meio'),
    ('blocos_meio','passagem_bloco_b_c'),
    ('passagem_bloco_b_c','blocos_sul'),
    ('oeste_sul','blocos_sul'),
    ('blocos_sul','biblioteca_oeste_meio'),
    ('biblioteca_oeste_meio','biblioteca_oeste'),
    # Ligacao diagonal oeste_meio -> blocos_meio removida.
    ('blocos_meio','praca_oeste'),
    ('praca_oeste','praca_centro'),
    ('praca_centro','praca_leste'),
    ('praca_centro','praca_norte'),
    ('praca_centro','praca_sul'),
    ('praca_leste','central_meio'),
    ('blocos_norte','superior_esquerda'),
    ('superior_esquerda','superior_centro'),
    ('superior_centro','superior_direita'),
    ('praca_norte','superior_centro'),
    ('central_meio','cantina_sul'),
    ('cantina_sul','direita_meio'),
    ('direita_meio','direita_norte'),
    ('direita_norte','superior_direita'),
    ('direita_meio','direita_sul'),
    ('direita_sul','direita_inferior'),
    ('direita_sul','quadras_leste'),
    ('quadras_leste','quadras_sul'),
    ('quadras_sul','central_sul'),
    ('direita_norte','extremo_direito_norte'),
    ('extremo_direito_norte','extremo_direito_meio'),
    ('extremo_direito_meio','extremo_direito_sul'),
    ('extremo_direito_meio','direita_meio'),
    ('extremo_direito_sul','direita_sul'),
]

PORTAS = {
    'Entrada Principal': (695,870),
    'Recepcao e Informacoes': (310,855),
    **{f'Laboratorio de Informatica {i}': (310,y) for i,y in enumerate([275,320,365,455,500,545],1)},
    'Salas de Aula - Bloco A': (525,285),
    'Salas de Aula - Bloco B': (525,380),
    'Salas de Aula - Bloco C': (525,475),
    'Biblioteca': (660,600), 'Auditorio': (1140,795),
    'Anfiteatro 1': (560,625), 'Anfiteatro 2': (820,625),
    'Espaco Maker': (345,675), 'Praca Central': (675,380),
    'Cantina': (920,385), 'Piscina': (700,245),
    'Quadra Poliesportiva 1': (860,635),
    'Quadra Poliesportiva 2': (1000,635),
    'Laboratorio de Engenharia Civil': (300,245),
    'Laboratorio de Fisioterapia': (1060,245),
    'Laboratorio de Odontologia': (1100,345),
    'Laboratorio de Medicina': (1100,475),
}

ACESSOS = {
    'Entrada Principal': 'entrada',
    'Recepcao e Informacoes': 'inferior_esquerda',
    **{f'Laboratorio de Informatica {i}': f'lab_{i}_acesso' for i in range(1,7)},
    'Salas de Aula - Bloco A': 'blocos_norte',
    'Salas de Aula - Bloco B': 'blocos_meio',
    'Salas de Aula - Bloco C': 'passagem_bloco_b_c',
    'Biblioteca': 'biblioteca_sul',
    'Auditorio': 'direita_inferior',
    'Anfiteatro 1': 'anf_esquerda',
    'Anfiteatro 2': 'anf_centro_cima',
    'Espaco Maker': 'oeste_sul',
    'Praca Central': 'praca_centro',
    'Cantina': 'cantina_sul',
    'Piscina': 'superior_centro',
    'Quadra Poliesportiva 1': 'central_sul',
    'Quadra Poliesportiva 2': 'quadras_sul',
    'Laboratorio de Engenharia Civil': 'oeste_norte',
    'Laboratorio de Fisioterapia': 'direita_norte',
    'Laboratorio de Odontologia': 'direita_meio',
    'Laboratorio de Medicina': 'direita_sul',
}


def distancia(ponto1, ponto2):
    return math.hypot(ponto2[0]-ponto1[0], ponto2[1]-ponto1[1])


def validar_grafo():
    problemas = []
    for a,b in LIGACOES:
        if a not in CAMINHOS:
            problemas.append(f'Ponto inexistente: {a}')
        if b not in CAMINHOS:
            problemas.append(f'Ponto inexistente: {b}')
    for local in LOCAIS:
        if local not in PORTAS:
            problemas.append(f'Porta ausente: {local}')
        if ACESSOS.get(local) not in CAMINHOS:
            problemas.append(f'Acesso invalido: {local}')
    return problemas


def calcular_rota(origem, destino):
    if origem not in LOCAIS or destino not in LOCAIS:
        return []
    if origem == destino:
        return [PORTAS[origem]]
    pontos = CAMINHOS.copy()
    pontos['origem'] = PORTAS[origem]
    pontos['destino'] = PORTAS[destino]
    grafo = {nome: [] for nome in pontos}
    for a,b in LIGACOES:
        if a not in pontos or b not in pontos:
            continue
        peso = distancia(pontos[a],pontos[b])
        grafo[a].append((b,peso))
        grafo[b].append((a,peso))
    for nome,local in (('origem',origem),('destino',destino)):
        acesso = ACESSOS.get(local)
        if acesso not in pontos:
            return []
        peso = distancia(pontos[nome],pontos[acesso])
        grafo[nome].append((acesso,peso))
        grafo[acesso].append((nome,peso))
    fila = [(0,'origem')]
    menores = {'origem':0}
    anteriores = {}
    while fila:
        custo,atual = heapq.heappop(fila)
        if custo > menores.get(atual,float('inf')):
            continue
        if atual == 'destino':
            break
        for vizinho,peso in grafo[atual]:
            novo_custo = custo + peso
            if novo_custo < menores.get(vizinho,float('inf')):
                menores[vizinho] = novo_custo
                anteriores[vizinho] = atual
                heapq.heappush(fila,(novo_custo,vizinho))
    if 'destino' not in menores:
        return []
    rota = []
    atual = 'destino'
    while atual != 'origem':
        rota.append(pontos[atual])
        atual = anteriores[atual]
    rota.append(pontos['origem'])
    rota.reverse()
    return rota
