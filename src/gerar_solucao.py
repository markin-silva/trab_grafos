def gerar_solucao(grafo, capacidade_veiculo):
    
    rotas = []  # Lista de rotas geradas
    servicos_pendentes = grafo.requeridos["nos"] + grafo.requeridos["arestas"] + grafo.requeridos["arcos"]

# Calcular número mínimo de veículos baseado na capacidade e demanda total
    demanda_total = sum(servico["demanda"] for servico in servicos_pendentes)
    num_veiculos = max(1, (demanda_total // capacidade_veiculo) + 1)  # Ajuste dinâmico

    veiculos = [{"demanda": 0, "custo": 0, "rota": [{"id": "D", "inicio": 0, "fim": 1, "demanda": 0, "custo": 0}]} for _ in range(num_veiculos)]

    # Distribuição dinâmica de serviços entre veículos
    while servicos_pendentes:
        progresso_feito = False  # Verificação para evitar loop infinito
        for veiculo in veiculos:
            if not servicos_pendentes:
                break  # Se todos os serviços foram atribuídos, encerramos
            
            melhor_servico = None
            
            # Escolhe um serviço viável que se conecta corretamente à rota atual
            for servico in servicos_pendentes:
                if (
                    servico["demanda"] + veiculo["demanda"] <= capacidade_veiculo and
                    (servico["inicio"] == veiculo["rota"][-1]["fim"] or servico["fim"] == veiculo["rota"][-1]["fim"])
                ):
                    melhor_servico = servico
                    break

            # Se nenhum serviço conectado foi encontrado, pega o primeiro disponível que respeite a capacidade
            if melhor_servico is None:
                melhor_servico = next((s for s in servicos_pendentes if s["demanda"] + veiculo["demanda"] <= capacidade_veiculo), None)

            # Caso um serviço seja encontrado, adiciona à rota
            if melhor_servico:
                veiculo["rota"].append(melhor_servico)
                veiculo["demanda"] += melhor_servico["demanda"]
                veiculo["custo"] += melhor_servico["custo"]
                servicos_pendentes.remove(melhor_servico)
                progresso_feito = True  # Indica que houve progresso na iteração

        # Se nenhuma mudança foi feita, interrompemos o loop para evitar repetição infinita
        if not progresso_feito:
            break

    # Finaliza rotas garantindo retorno ao depósito
    for veiculo in veiculos:
        if veiculo["rota"][-1]["id"] != "D":
            veiculo["rota"].append({"id": "D", "inicio": 0, "fim": 1, "demanda": 0, "custo": 0})

        rotas.append(veiculo)

    # Calcula o custo total corretamente
    custo_total = sum(
        servico["custo"]
        for veiculo in veiculos for servico in veiculo["rota"]
        if isinstance(servico, dict) and servico["id"] != "D"
    )

    return rotas, custo_total
