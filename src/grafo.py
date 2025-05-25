class No:
    def __init__(self, id, requerido=False, demanda=0, custo_servico=0):
        self.id = id
        self.requerido = requerido
        self.demanda = demanda
        self.custo_servico = custo_servico
class Aresta:
    def __init__(self, origem, destino, custo_viagem, demanda=0, custo_servico=0, requerido=False, direcionado=False):
        self.origem = origem
        self.destino = destino
        self.custo_viagem = custo_viagem
        self.demanda = demanda
        self.custo_servico = custo_servico
        self.requerido = requerido
        self.direcionado = direcionado  # True se for arco, False se for aresta

class Grafo:
    def __init__(self):
        self.nos = {}     # id -> No
        self.arestas = [] # lista de Aresta (e Arco)
        self.deposito = None
        self.capacidade = None

    def adiciona_no(self, id_no, requerido=False, demanda=0, custo_servico=0):
        if id_no not in self.nos:
            self.nos[id_no] = No(id_no, requerido, demanda, custo_servico)
        else:
            # Atualiza atributos se necessário
            no = self.nos[id_no]
            no.requerido = no.requerido or requerido
            if demanda > 0:
                no.demanda = demanda
            if custo_servico > 0:
                no.custo_servico = custo_servico

    def adiciona_aresta(self, origem, destino, custo_viagem, demanda=0, custo_servico=0, requerido=False, direcionado=False):
        self.arestas.append(Aresta(origem, destino, custo_viagem, demanda, custo_servico, requerido, direcionado))