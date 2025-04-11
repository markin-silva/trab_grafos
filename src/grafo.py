class Grafo:
    def __init__(self):
        # Armazenamos informações em:
        # - self.nos: dicionário { nome_no: {"grau": ...} }
        # - self.arestas: lista de dicionários {"de", "para", "custo"}
        # - self.arcos: lista de dicionários {"de", "para", "custo"}
        # - self.requeridos: dicionário com chaves "nos", "arestas", "arcos" para armazenar as entidades obrigatórias
        self.nos = {}
        self.arestas = []
        self.arcos = []
        self.requeridos = {
            "nos": [],
            "arestas": [],
            "arcos": []
        }

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