class Grafo:
    def __init__(self):
        self.nos = {}  # {'no_id': {"grau": grau, "requerido": True/False}}
        self.arestas = []  # Lista de arestas [(de, para, custo)]
        self.arcos = []  # Lista de arcos [(de, para, custo)]
        self.requeridos = {"nos": [], "arestas": [], "arcos": []}

    def adicionar_no(self, no):
        if no not in self.nos:
            self.nos[no] = {"grau": 0, "requerido": False}

    def adicionar_aresta(self, de, para, custo):
        if de not in self.nos:
            self.adicionar_no(de)
        if para not in self.nos:
            self.adicionar_no(para)

        self.arestas.append({"de": de, "para": para, "custo": custo, "requerido": False})
        # Atualiza o grau dos nós
        self.nos[de]["grau"] += 1
        self.nos[para]["grau"] += 1

    def adicionar_arco(self, de, para, custo):
        if de not in self.nos:
            self.adicionar_no(de)
        if para not in self.nos:
            self.adicionar_no(para)

        self.arcos.append({"de": de, "para": para, "custo": custo, "requerido": False})
        self.nos[de]["grau"] += 1


    def adicionar_requerido(self, tipo, item):
        if tipo in self.requeridos:
            self.requeridos[tipo].append(item)
            # Marca o nó/aresta/arco como requerido
            if tipo == "nos":
                self.nos[item['id']]["requerido"] = True
            elif tipo == "arestas":
                # Precisamos marcar as arestas requeridas
                for aresta in self.arestas:
                    if aresta['de'] == item['inicio'] and aresta['para'] == item['fim']:
                        aresta["requerido"] = True
            elif tipo == "arcos":
                # Marcar os arcos requeridos
                for arco in self.arcos:
                    if arco['de'] == item['inicio'] and arco['para'] == item['fim']:
                        arco["requerido"] = True