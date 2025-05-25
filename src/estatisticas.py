def quantidade_vertices(grafo):
    return len(grafo.nos)

def quantidade_arestas(grafo):
    return sum(1 for aresta in grafo.arestas if not aresta.direcionado)  # Apenas arestas bidirecionais

def quantidade_arcos(grafo):
    return sum(1 for aresta in grafo.arestas if aresta.direcionado)  # Apenas arcos direcionados

def quantidade_vertices_requeridos(grafo):
    return sum(1 for no in grafo.nos.values() if no.requerido)

def quantidade_arestas_requeridas(grafo):
    return sum(1 for aresta in grafo.arestas if aresta.requerido and not aresta.direcionado)

def quantidade_arcos_requeridos(grafo):
    return sum(1 for aresta in grafo.arestas if aresta.requerido and aresta.direcionado)

def densidade(grafo):
    n = len(grafo.nos)
    m = len(grafo.arestas)
    return m / (n * (n - 1)) if n > 1 else 0

def grau_min_max(grafo):
    graus = {no_id: 0 for no_id in grafo.nos}
    for aresta in grafo.arestas:
        graus[aresta.origem] += 1
        graus[aresta.destino] += 1
    
    return min(graus.values()), max(graus.values())

def componentes_conectados(grafo):
    visitados = set()
    componentes = 0

    def dfs(no):
        visitados.add(no)
        for aresta in grafo.arestas:
            if aresta.origem == no and aresta.destino not in visitados:
                dfs(aresta.destino)
            if aresta.destino == no and aresta.origem not in visitados:
                dfs(aresta.origem)
    
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
    return max(
        matriz_caminhos[origem][destino] 
        for origem in matriz_caminhos 
        for destino in matriz_caminhos[origem] 
        if matriz_caminhos[origem][destino] != float('inf')
    )

def floyd_warshall(grafo):
    nos = list(grafo.nos.keys())
    matriz_caminhos = {no: {dest: float('inf') for dest in nos} for no in nos}
    matriz_predecessores = {no: {dest: None for dest in nos} for no in nos}

    for no in nos:
        matriz_caminhos[no][no] = 0

    for aresta in grafo.arestas:
        matriz_caminhos[aresta.origem][aresta.destino] = aresta.custo_viagem
        matriz_predecessores[aresta.origem][aresta.destino] = aresta.origem
        if not aresta.direcionado:  # Se for bidirecional
            matriz_caminhos[aresta.destino][aresta.origem] = aresta.custo_viagem
            matriz_predecessores[aresta.destino][aresta.origem] = aresta.destino

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
