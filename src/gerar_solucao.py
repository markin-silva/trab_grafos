import random
import time

def gerar_solucao(grafo, capacidade):
    rotas = []  # Lista para armazenar as rotas
    custo_total = 0  # Acumulador de custo total
    t0 = time.time()  # Marca o tempo inicial para medir o tempo de execução

    # Lista de serviços (nós, arestas e arcos requeridos)
    servicos = grafo.requeridos["nos"] + grafo.requeridos["arestas"] + grafo.requeridos["arcos"]

    print(f"Total de serviços a serem processados: {len(servicos)}")  # Verificando quantidade de serviços
    
    # Rotas a serem construídas
    while servicos:
        # Cria uma rota vazia
        rota_atual = {"rota": [], "demanda": 0, "custo": 0}
        
        # Adiciona o depósito na rota
        rota_atual["rota"].append({"id": "D", "inicio": 0, "fim": 1})
        print("Iniciando nova rota.")
        
        # Enquanto houver serviços para atender na rota
        while servicos and rota_atual["demanda"] < capacidade:
            # Escolher aleatoriamente um serviço
            servico = random.choice(servicos)
            servicos.remove(servico)

            print(f"Adicionando serviço {servico['id']} à rota")  # Verificando o serviço que está sendo adicionado

            # Adiciona o serviço à rota atual
            rota_atual["rota"].append({
                "id": servico['id'],
                "inicio": servico['inicio'],
                "fim": servico['fim']
            })

            # Atualiza a demanda total da rota
            rota_atual["demanda"] += servico['demanda']
            rota_atual["custo"] += servico['custo']

            print(f"Demanda atual da rota: {rota_atual['demanda']} / Custo total da rota: {rota_atual['custo']}")  # Verificando demanda e custo

            # Verifica se a demanda ultrapassa a capacidade do veículo
            if rota_atual["demanda"] > capacidade:
                # Se exceder a capacidade, adiciona a rota finalizada e começa uma nova rota
                rotas.append(rota_atual)
                custo_total += rota_atual["custo"]
                print(f"Rota finalizada com custo {rota_atual['custo']}. Custo total até agora: {custo_total}")
                rota_atual = {"rota": [], "demanda": 0, "custo": 0}
                break

        # Se ainda houver serviços restantes e a demanda estiver dentro da capacidade, adiciona a última rota
        if rota_atual["demanda"] <= capacidade:
            rotas.append(rota_atual)
            custo_total += rota_atual["custo"]
            print(f"Rota finalizada com custo {rota_atual['custo']}. Custo total final: {custo_total}")

    # Marca o tempo de execução
    t_alg = time.time() - t0

    print(f"Total de rotas: {len(rotas)}")
    print(f"Custo total das rotas: {custo_total}")

    return rotas, custo_total, t_alg
