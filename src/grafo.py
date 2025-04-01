class Grafo:
    def __init__(self):
        self.nos = {}  # Dicionário de nós
        self.arestas = []  # Lista de arestas
        self.arcos = []  # Lista de arcos
        self.requeridos = {"nos": [], "arestas": [], "arcos": []}  # Elementos requeridos

    def adicionar_no(self, no):
        if no not in self.nos:
            self.nos[no] = {"grau": 0}

    def adicionar_aresta(self, de, para, custo):
        if de not in self.nos:
            self.adicionar_no(de)
        if para not in self.nos:
            self.adicionar_no(para)

        self.arestas.append({"de": de, "para": para, "custo": custo})
        self.nos[de]["grau"] += 1
        self.nos[para]["grau"] += 1

    def adicionar_arco(self, de, para, custo):
        if de not in self.nos:
            self.adicionar_no(de)
        if para not in self.nos:
            self.adicionar_no(para)

        self.arcos.append({"de": de, "para": para, "custo": custo})
        self.nos[de]["grau"] += 1


    def adicionar_requerido(self, tipo, item):
        self.requeridos[tipo].append(item)

    def mostrar_info(self):
        print("Nós:", self.nos)
        print("Arestas:", self.arestas)
        print("Arcos:", self.arcos)
        print("Requeridos:", self.requeridos)