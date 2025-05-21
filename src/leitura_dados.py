from grafo import Grafo

def ler_arquivo(filepath):
    grafo = Grafo()
    tipo = None
    capacidade_veiculo = None
    id_servico = 1  # ID global de serviço

    # Mapeamento para as seções do arquivo
    prefix_map = {
        "ReN.": "nos",
        "ReE.": "arestas",
        "ReA.": "arcos",
        "EDGE": "arestas_nao_requeridas",
        "ARC":  "arcos_nao_requeridos"
    }

    try:
        with open(filepath, 'r') as arquivo:
            linhas = arquivo.readlines()

        for linha in linhas:
            linha = linha.strip()

            if not linha or linha.startswith("#"):
                continue  # Ignora linhas em branco ou de comentário

            # Captura a capacidade do veículo
            if linha.startswith("Capacity:"):
                capacidade_veiculo = int(linha.split()[1])
                continue

            # Verifica o tipo de dado (nos, arestas, arcos) na linha
            if any(linha.startswith(k) for k in prefix_map.keys()):
                tipo = next(v for k, v in prefix_map.items() if linha.startswith(k))
                continue

            dados = linha.split()

            # Leitura de dados de nós (ReN.)
            if tipo == "nos" and len(dados) == 3:
                no_id = dados[0].replace("N", "")  # Remove o prefixo "N" do nó
                grafo.adicionar_no(no_id)
                grafo.adicionar_requerido("nos", {
                    "id": no_id,
                    "inicio": no_id,
                    "fim": no_id,
                    "demanda": int(dados[1]),
                    "custo": int(dados[2])
                })
                id_servico += 1

            # Leitura de dados de arestas (ReE.)
            elif tipo == "arestas" and len(dados) == 6:
                grafo.adicionar_aresta(dados[1], dados[2], int(dados[3]))
                grafo.adicionar_requerido("arestas", {
                    "id": id_servico,
                    "inicio": dados[1],
                    "fim": dados[2],
                    "demanda": int(dados[4]),
                    "custo": int(dados[5])
                })
                id_servico += 1

            # Leitura de dados de arcos (ReA.)
            elif tipo == "arcos" and len(dados) == 6:
                grafo.adicionar_arco(dados[1], dados[2], int(dados[3]))
                grafo.adicionar_requerido("arcos", {
                    "id": id_servico,
                    "inicio": dados[1],
                    "fim": dados[2],
                    "demanda": int(dados[4]),
                    "custo": int(dados[5])
                })
                id_servico += 1

            # Processando dados de arcos não requeridos (ARC)
            elif tipo == "arcos_nao_requeridos" and len(dados) == 3:
                # Nesse caso, estamos apenas adicionando os arcos ao grafo
                grafo.adicionar_arco(dados[1], dados[2], int(dados[3]))

    except FileNotFoundError:
        print(f"Erro: O arquivo {filepath} não foi encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")

    return grafo, capacidade_veiculo
