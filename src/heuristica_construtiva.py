import time

from floyd_warshall import floyd_warshall

def criar_servicos(grafo):
    servicos = []
    idx = 1  # índice único do serviço, para saída
    
    # Nós requeridos
    for no in grafo.nos.values():
        if no.requerido:
            servicos.append({
                'tipo': 'N',
                'id': idx,
                'origem': no.id,
                'destino': no.id,
                'demanda': no.demanda,
                'custo_servico': no.custo_servico
            })
            idx += 1
    
    # Arestas requeridas (bidirecionais)
    arestas_pegadas = set()
    for a in grafo.arestas:
        if not a.direcionado and a.requerido:
            key = tuple(sorted((a.origem, a.destino)))
            if key not in arestas_pegadas:
                servicos.append({
                    'tipo': 'E',
                    'id': idx,
                    'origem': a.origem,
                    'destino': a.destino,
                    'demanda': a.demanda,
                    'custo_servico': a.custo_servico
                })
                idx += 1
                arestas_pegadas.add(key)
    
    # Arcos requeridos (direcionados)
    for a in grafo.arestas:
        if a.direcionado and a.requerido:
            servicos.append({
                'tipo': 'A',
                'id': idx,
                'origem': a.origem,
                'destino': a.destino,
                'demanda': a.demanda,
                'custo_servico': a.custo_servico
            })
            idx += 1
    
    return servicos

def clusterizacao_gulosa_demanda_proximidade(servicos, distancias, mapa_indices, capacidade):
    servicos_restantes = servicos.copy()
    clusters = []

    while servicos_restantes:
        # Ordena por demanda decrescente para iniciar cluster com serviço maior
        servicos_restantes.sort(key=lambda s: s['demanda'], reverse=True)
        cluster = []
        carga = 0

        # Começa cluster com o serviço de maior demanda
        atual = servicos_restantes.pop(0)
        cluster.append(atual)
        carga += atual['demanda']

        while True:
            # Busca serviço mais próximo de 'atual' que caiba na capacidade
            melhor_candidato = None
            menor_dist = float('inf')

            for s in servicos_restantes:
                if carga + s['demanda'] > capacidade:
                    continue
                # Calcula distância entre serviços
                i = mapa_indices[atual['destino']]
                j = mapa_indices[s['origem']]
                dist = distancias[i][j]

                if dist < menor_dist:
                    menor_dist = dist
                    melhor_candidato = s

            if melhor_candidato is None:
                # Nenhum candidato cabe, fecha cluster
                break

            # Adiciona o candidato no cluster
            cluster.append(melhor_candidato)
            carga += melhor_candidato['demanda']
            servicos_restantes.remove(melhor_candidato)
            atual = melhor_candidato

        clusters.append(cluster)

    return clusters

def construir_rota(cluster, grafo, distancias, mapa_indices):
    deposito = grafo.deposito
    rota = []
    no_atual = deposito
    servicos_restantes = cluster.copy()

    # Inicia rota com depósito
    rota.append(('D', 0, deposito, deposito))

    while servicos_restantes:
        melhor_servico = None
        menor_dist = float('inf')

        for s in servicos_restantes:
            i = mapa_indices[no_atual]
            j = mapa_indices[s['origem']]
            dist = distancias[i][j]
            if dist < menor_dist:
                menor_dist = dist
                melhor_servico = s

        # Adiciona o serviço mais próximo
        rota.append((
            melhor_servico['tipo'],
            melhor_servico['id'],
            melhor_servico['origem'],
            melhor_servico['destino']
        ))

        no_atual = melhor_servico['destino']
        servicos_restantes.remove(melhor_servico)

    # Volta ao depósito no fim da rota
    rota.append(('D', 0, deposito, deposito))

    return rota

def calcular_custo_e_demanda_rota(rota, servicos, distancias, mapa_indices):
    demanda_total = 0
    custo_total = 0
    visitados = set()  # Para contar custo serviço e demanda apenas uma vez

    for idx in range(1, len(rota)):
        prev = rota[idx-1]
        curr = rota[idx]

        # Custo viagem do nó destino anterior para nó origem atual
        i = mapa_indices[prev[3]]  # prev destino
        j = mapa_indices[curr[2]]  # curr origem
        custo_viagem = distancias[i][j]
        custo_total += custo_viagem

        # Se serviço, soma demanda e custo serviço se não visitado antes
        if curr[0] != 'D':
            id_servico = curr[1]
            if id_servico not in visitados:
                visitados.add(id_servico)
                # Procura o serviço para pegar demanda e custo serviço
                # Suponha que tenha um dict id -> serviço
                serv = next(s for s in servicos if s['id'] == id_servico)
                demanda_total += serv['demanda']
                custo_total += serv['custo_servico']

    return demanda_total, custo_total

def heuristica_construtiva(grafo):
    inicio_tempo = time.time()

    distancias, mapa_indices = floyd_warshall(grafo)
    servicos = criar_servicos(grafo)
    clusters = clusterizacao_gulosa_demanda_proximidade(servicos, distancias, mapa_indices, grafo.capacidade)

    rotas = []
    custo_total = 0
    for cluster in clusters:
        rota = construir_rota(cluster, grafo, distancias, mapa_indices)
        demanda_rota, custo_rota = calcular_custo_e_demanda_rota(rota, servicos, distancias, mapa_indices)
        rotas.append((demanda_rota, custo_rota, rota))
        custo_total += custo_rota

    fim_tempo = time.time()
    tempo_execucao = int((fim_tempo - inicio_tempo)*1e6)  # microssegundos

    return custo_total, rotas, tempo_execucao
