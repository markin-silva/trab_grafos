from grafo import Grafo

def ler_arquivo(filepath):
    
    grafo = Grafo()
    tipo = None
    capacidade_veiculo = None  # Inicializa como indefinido

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

        # Captura a capacidade do veículo dinamicamente
        if linha.startswith("Capacity:"):
            try:
                capacidade_veiculo = int(linha.split()[1])  # Extração segura
            except ValueError:
                capacidade_veiculo = None
            continue

        novo_tipo = next((v for k, v in prefix_map.items() if linha.startswith(k)), None)
        if novo_tipo is not None:
            tipo = novo_tipo
            continue

        dados = linha.split()

        if tipo == "nos" and len(dados) >= 3:
            no_id = dados[0].replace("N", "")
            grafo.adicionar_no(no_id)
            grafo.adicionar_requerido("nos", {
                "id": no_id,
                "inicio": no_id,
                "fim": no_id,
                "demanda": int(dados[1]),
                "custo": int(dados[2])
            })

        elif tipo == "arestas" and len(dados) >= 6:
            aresta_id = dados[0].replace("E", "")
            grafo.adicionar_aresta(dados[1], dados[2], int(dados[3]))
            grafo.adicionar_requerido("arestas", {
                "id": aresta_id,
                "inicio": dados[1],
                "fim": dados[2],
                "demanda": int(dados[4]),
                "custo": int(dados[5])
            })

        elif tipo == "arcos" and len(dados) >= 6:
            arco_id = dados[0].replace("A", "")
            grafo.adicionar_arco(dados[1], dados[2], int(dados[3]))
            grafo.adicionar_requerido("arcos", {
                "id": arco_id,
                "inicio": dados[1],
                "fim": dados[2],
                "demanda": int(dados[4]),
                "custo": int(dados[5])
            })

    # Verificação final da capacidade do veículo
    if capacidade_veiculo is None:
        capacidade_veiculo = 10  # Define um valor padrão se não for encontrado

    return grafo, capacidade_veiculo  # Retorna também a capacidade lida
