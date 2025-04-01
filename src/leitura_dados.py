from grafo import Grafo

def ler_arquivo(filepath):
    grafo = Grafo()
    tipo = None

    with open(filepath, 'r') as arquivo:
        linhas = arquivo.readlines()

    for linha in linhas:
        linha = linha.strip()

        if linha.startswith("ReN."):
            tipo = "nos"
        elif linha.startswith("ReE."):
            tipo = "arestas"
        elif linha.startswith("ReA."):
            tipo = "arcos"
        elif linha.startswith("EDGE"):
            tipo = "arestas_nao_requeridas"
        elif linha.startswith("ARC"):
            tipo = "arcos_nao_requeridos"
        elif linha.startswith("#") or linha == "":
            continue

        else:
            dados = linha.split()
            if tipo == "nos" and len(dados) >= 1:
                grafo.adicionar_no(dados[0])
                grafo.adicionar_requerido("nos", dados[0])
            elif tipo in {"arestas", "arestas_nao_requeridas"} and len(dados) >= 4:
                grafo.adicionar_aresta(dados[1], dados[2], int(dados[3]))
                if tipo == "arestas":  
                    grafo.adicionar_requerido("arestas", (dados[1], dados[2]))
            elif tipo in {"arcos", "arcos_nao_requeridos"} and len(dados) >= 4:
                grafo.adicionar_arco(dados[1], dados[2], int(dados[3]))
                if tipo == "arcos":
                    grafo.adicionar_requerido("arcos", (dados[1], dados[2]))

    return grafo