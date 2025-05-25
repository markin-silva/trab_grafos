from grafo import Grafo

def ler_arquivo(caminho_arquivo):
    grafo = Grafo()
    secao = None

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            try:
                linha = linha.strip()
                if not linha or linha.startswith('#') or linha.startswith('the data'):
                    continue

                if 'Depot Node:' in linha:
                    deposito = int(linha.split(':')[1].strip())
                    grafo.deposito = deposito
                    continue

                if 'Capacity:' in linha:
                    capacidade = int(linha.split(':')[1].strip())
                    grafo.capacidade = capacidade
                    continue

                # Identifica se mudou a seção
                if linha.startswith('ReN.'):
                    secao = 'nos_requeridos'
                    continue
                elif linha.startswith('ReE.'):
                    secao = 'arestas_requeridas'
                    continue
                elif linha.startswith('EDGE'):
                    secao = 'arestas_nao_requeridas'
                    continue
                elif linha.startswith('ReA.'):
                    secao = 'arcos_requeridos'
                    continue
                elif linha.startswith('ARC'):
                    secao = 'arcos_nao_requeridos'
                    continue

                # Processa linhas conforme a seção
                if secao == 'nos_requeridos':
                    partes = linha.split()
                    if len(partes) >= 3:
                        id_no = int(partes[0][1:])  # Remove o 'N'
                        demanda = int(partes[1])
                        custo_servico = int(partes[2])
                        grafo.adiciona_no(id_no, requerido=True, demanda=demanda, custo_servico=custo_servico)

                elif secao == 'arestas_requeridas':
                    partes = linha.split()
                    if len(partes) >= 6:
                        origem = int(partes[1])
                        destino = int(partes[2])
                        custo_viagem = int(partes[3])
                        demanda = int(partes[4])
                        custo_servico = int(partes[5])
                        # Arestas bidirecionais requeridas (vai e volta)
                        grafo.adiciona_aresta(origem, destino, custo_viagem, demanda, custo_servico, requerido=True, direcionado=False)
                        grafo.adiciona_aresta(destino, origem, custo_viagem, demanda, custo_servico, requerido=True, direcionado=False)
                        # Garante que os nós existam
                        grafo.adiciona_no(origem)
                        grafo.adiciona_no(destino)

                elif secao == 'arestas_nao_requeridas':
                    partes = linha.split()
                    if len(partes) >= 4:
                        origem = int(partes[1])
                        destino = int(partes[2])
                        custo_viagem = int(partes[3])
                        # Arestas bidirecionais não requeridas
                        grafo.adiciona_aresta(origem, destino, custo_viagem, requerido=False, direcionado=False)
                        grafo.adiciona_aresta(destino, origem, custo_viagem, requerido=False, direcionado=False)
                        grafo.adiciona_no(origem)
                        grafo.adiciona_no(destino)

                elif secao == 'arcos_requeridos':
                    partes = linha.split()
                    if len(partes) >= 6:
                        origem = int(partes[1])
                        destino = int(partes[2])
                        custo_viagem = int(partes[3])
                        demanda = int(partes[4])
                        custo_servico = int(partes[5])
                        # Arcos direcionados requeridos
                        grafo.adiciona_aresta(origem, destino, custo_viagem, demanda, custo_servico, requerido=True, direcionado=True)
                        grafo.adiciona_no(origem)
                        grafo.adiciona_no(destino)

                elif secao == 'arcos_nao_requeridos':
                    partes = linha.split()
                    if len(partes) >= 4:
                        origem = int(partes[1])
                        destino = int(partes[2])
                        custo_viagem = int(partes[3])
                        # Arcos direcionados não requeridos
                        grafo.adiciona_aresta(origem, destino, custo_viagem, requerido=False, direcionado=True)
                        grafo.adiciona_no(origem)
                        grafo.adiciona_no(destino)
            except ValueError as e:
                print(f"Erro ao processar linha: {linha}. Erro: {e}")
                continue

    return grafo
