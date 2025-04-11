from grafo import Grafo

def ler_arquivo(filepath):
    grafo = Grafo()
    tipo = None

    prefix_map = {
        "ReN.": "nos",
        "ReE.": "arestas",
        "ReA.": "arcos",
        "EDGE": "arestas_nao_requeridas",
        "ARC":  "arcos_nao_requeridos"
    }

    with open(filepath, 'r') as arquivo:
        linhas = arquivo.readlines()

    for linha in linhas:
        linha = linha.strip()

        if not linha or linha.startswith("#"):
            continue

        novo_tipo = next((v for k, v in prefix_map.items() if linha.startswith(k)), None)
        if novo_tipo is not None:
            tipo = novo_tipo
            continue

        dados = linha.split()

        if tipo == "nos" and len(dados) >= 1:
            no_str = dados[0]
            if no_str.startswith("N"):
                no_str = no_str[1:]
            grafo.adicionar_no(no_str)
            grafo.adicionar_requerido("nos", no_str)
        elif tipo in {"arestas", "arestas_nao_requeridas"} and len(dados) >= 4:
            grafo.adicionar_aresta(dados[1], dados[2], int(dados[3]))
            if tipo == "arestas":  
                grafo.adicionar_requerido("arestas", (dados[1], dados[2]))
        elif tipo in {"arcos", "arcos_nao_requeridos"} and len(dados) >= 4:
            grafo.adicionar_arco(dados[1], dados[2], int(dados[3]))
            if tipo == "arcos":
                grafo.adicionar_requerido("arcos", (dados[1], dados[2]))

    return grafo