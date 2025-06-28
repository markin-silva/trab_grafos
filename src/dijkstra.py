# ./src/algoritmos_grafos.py

import heapq

def criar_lista_adjacencia(grafo):
    """
    Cria uma lista de adjacência a partir da estrutura do grafo.
    Esta é a estrutura de dados ideal para algoritmos como Dijkstra.
    Formato: {no_id: [(vizinho_id, custo_viagem), ...]}
    """
    adj = {no_id: [] for no_id in grafo.nos}
    for aresta in grafo.arestas:
        adj[aresta.origem].append((aresta.destino, aresta.custo_viagem))
    return adj

def dijkstra(no_inicial, grafo_adj, todos_os_nos):
    """
    Versão OTIMIZADA do Dijkstra que usa a lista de adjacência.
    """
    distancias = {no_id: float('inf') for no_id in todos_os_nos}
    distancias[no_inicial] = 0
    
    fila_prioridade = [(0, no_inicial)]
    
    while fila_prioridade:
        dist_atual, no_atual_id = heapq.heappop(fila_prioridade)
        
        if dist_atual > distancias[no_atual_id]:
            continue
            
        # A MÁGICA ACONTECE AQUI: busca de vizinhos é instantânea!
        if no_atual_id in grafo_adj:
            for vizinho_id, peso_aresta in grafo_adj[no_atual_id]:
                distancia_nova = dist_atual + peso_aresta
                
                if distancia_nova < distancias[vizinho_id]:
                    distancias[vizinho_id] = distancia_nova
                    heapq.heappush(fila_prioridade, (distancia_nova, vizinho_id))
                    
    return distancias

def calcular_distancias_necessarias_dijkstra(grafo, nos_origem_relevantes):
    """
    Usa a versão otimizada do Dijkstra para calcular as distâncias.
    """
    # 1. Cria a estrutura de dados eficiente UMA VEZ.
    lista_adj = criar_lista_adjacencia(grafo)
    
    todos_os_nos_ids = sorted(list(grafo.nos.keys()))
    mapa_indices = {no_id: i for i, no_id in enumerate(todos_os_nos_ids)}
    num_nos = len(todos_os_nos_ids)
    
    matriz_distancias = [[float('inf')] * num_nos for _ in range(num_nos)]
    
    # 2. Itera sobre os nós relevantes, usando a lista de adjacência
    for no_id in nos_origem_relevantes:
        distancias_desde_no = dijkstra(no_id, lista_adj, todos_os_nos_ids)
        
        if no_id in mapa_indices:
            i = mapa_indices[no_id]
            for dest_id, dist in distancias_desde_no.items():
                if dest_id in mapa_indices:
                    j = mapa_indices[dest_id]
                    matriz_distancias[i][j] = dist
            
    return matriz_distancias, mapa_indices