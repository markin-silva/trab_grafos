import math

def floyd_warshall(grafo):
    nos = list(grafo.nos.keys())
    n = len(nos)
    index = {no: idx for idx, no in enumerate(nos)}
    
    dist = [[math.inf]*n for _ in range(n)]
    
    # Inicializa distâncias
    for i in range(n):
        dist[i][i] = 0
    
    # Preenche distâncias diretas (custo_viagem)
    for a in grafo.arestas:
        i = index[a.origem]
        j = index[a.destino]
        if a.custo_viagem < dist[i][j]:
            dist[i][j] = a.custo_viagem
    
    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist, index