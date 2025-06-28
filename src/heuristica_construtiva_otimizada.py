import time

from dijkstra import calcular_distancias_necessarias_dijkstra
from floyd_warshall import floyd_warshall

from heuristica_construtiva import criar_servicos, clusterizacao_gulosa_demanda_proximidade, construir_rota, calcular_custo_e_demanda_rota

LIMIAR_DE_NOS_PARA_DIJKSTRA = 20

def heuristica_construtiva_otimizada(grafo):
    """
    Versão HÍBRIDA: escolhe a melhor estratégia (Floyd-Warshall ou Dijkstra)
    com base no tamanho do grafo para garantir a melhor performance em todos os casos.
    """
    inicio_tempo = time.time()

    num_nos = len(grafo.nos)

    # --- ESTRATÉGIA HÍBRIDA INTELIGENTE ---
    if num_nos < LIMIAR_DE_NOS_PARA_DIJKSTRA:
        # Para grafos pequenos, utiliza Floyd-Warshall.
        print(f"Grafo pequeno ({num_nos} nós). Usando Floyd-Warshall.")
        distancias, mapa_indices = floyd_warshall(grafo)
    else:
        # Para grafos maiores, utiliza Dkistra
        servicos_temp = criar_servicos(grafo)
        nos_finais_de_servico = {s['destino'] for s in servicos_temp}
        nos_origem_relevantes = list(nos_finais_de_servico | {grafo.deposito})
        
        print(f"Grafo grande ({num_nos} nós). Usando Dijkstra em {len(nos_origem_relevantes)} nós relevantes.")
        distancias, mapa_indices = calcular_distancias_necessarias_dijkstra(grafo, nos_origem_relevantes)

    servicos = criar_servicos(grafo)
    clusters = clusterizacao_gulosa_demanda_proximidade(servicos, distancias, mapa_indices, grafo.capacidade)

    rotas = []
    custo_total = 0
    for cluster in clusters:
        rota = construir_rota(cluster, grafo, distancias, mapa_indices)
        demanda_rota, custo_rota = calcular_custo_e_demanda_rota(rota, servicos, distancias, mapa_indices)
        rotas.append((demanda_rota, custo_rota, rota))
        custo_total += custo_rota

    fim_tempo = time.time()
    tempo_execucao_otimizado = int((fim_tempo - inicio_tempo) * 1e6)  # microssegundos

    return custo_total, rotas, tempo_execucao_otimizado
