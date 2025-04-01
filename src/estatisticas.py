def quantidade_vertices(grafo):
    return len(grafo.nos)

def quantidade_arestas(grafo):
    return len(grafo.arestas)

def quantidade_arcos(grafo):
    return len(grafo.arcos)

def quantidade_vertices_requeridos(grafo):
    return len(grafo.requeridos["nos"])

def quantidade_arestas_requeridas(grafo):
    return len(grafo.requeridos["arestas"])

def quantidade_arcos_requeridos(grafo):
    return len(grafo.requeridos["arcos"])

def densidade(grafo):
    n = len(grafo.nos)
    m = len(grafo.arestas) + len(grafo.arcos)
    return m / (n * (n - 1)) if n > 1 else 0

def grau_min_max(grafo):
    graus = [info["grau"] for info in grafo.nos.values()]
    return min(graus), max(graus)

def componentes_conectados(grafo):
    visitados = set()
    componentes = 0

    def dfs(no):
        visitados.add(no)
        for vizinho in grafo.nos:
            if vizinho not in visitados:
                dfs(vizinho)
    
    for no in grafo.nos:
        if no not in visitados:
            dfs(no)
            componentes += 1

    return componentes

def intermediacao(grafo, caminhos_completos):
    intermediacao = {no: 0 for no in grafo.nos}
    for origem, destinos in caminhos_completos.items():
        for destino, caminho in destinos.items():
            if origem != destino and caminho: 
                for no in caminho[1:-1]: 
                    intermediacao[no] += 1
    return intermediacao

def caminho_medio(matriz_caminhos):
    soma_caminhos = 0
    total_caminhos = 0
    for origem in matriz_caminhos:
        for destino in matriz_caminhos[origem]:
            if origem != destino and matriz_caminhos[origem][destino] != float('inf'):
                soma_caminhos += matriz_caminhos[origem][destino]
                total_caminhos += 1
    return soma_caminhos / total_caminhos if total_caminhos > 0 else 0

def diametro(matriz_caminhos):
    maior_caminho = 0
    for origem in matriz_caminhos:
        for destino in matriz_caminhos[origem]:
            if matriz_caminhos[origem][destino] != float('inf'):
                maior_caminho = max(maior_caminho, matriz_caminhos[origem][destino])
    return maior_caminho

def floyd_warshall(grafo):
    nos = list(grafo.nos.keys())
    matriz_caminhos = {no: {dest: float('inf') for dest in nos} for no in nos}
    matriz_predecessores = {no: {dest: None for dest in nos} for no in nos}

    for no in nos:
        matriz_caminhos[no][no] = 0

    for aresta in grafo.arestas:
        matriz_caminhos[aresta["de"]][aresta["para"]] = aresta["custo"]
        matriz_caminhos[aresta["para"]][aresta["de"]] = aresta["custo"]
        matriz_predecessores[aresta["de"]][aresta["para"]] = aresta["de"]
        matriz_predecessores[aresta["para"]][aresta["de"]] = aresta["para"]

    for arco in grafo.arcos:
        matriz_caminhos[arco["de"]][arco["para"]] = arco["custo"]
        matriz_predecessores[arco["de"]][arco["para"]] = arco["de"]

    for k in nos:
        for i in nos:
            for j in nos:
                novo_caminho = matriz_caminhos[i][k] + matriz_caminhos[k][j]
                if matriz_caminhos[i][j] > novo_caminho:
                    matriz_caminhos[i][j] = novo_caminho
                    matriz_predecessores[i][j] = matriz_predecessores[k][j]

    caminhos_completos = {no: {dest: [] for dest in nos} for no in nos}
    for origem in nos:
        for destino in nos:
            if origem != destino and matriz_caminhos[origem][destino] != float('inf'):
                caminho = []
                atual = destino
                while atual is not None:
                    caminho.insert(0, atual)
                    atual = matriz_predecessores[origem][atual]
                caminhos_completos[origem][destino] = caminho

    return matriz_caminhos, caminhos_completos