import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}
        self._popolarita = {}

    def getGenres(self):
        return DAO.getAllGenres()

    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    def buildGraph(self, g):
        self._grafo.clear()
        self._idMap.clear()
        # La popolarita va calcolata sul genere selezionato (non globalmente)
        self._popolarita = {}
        for a in DAO.getAllPop(g):
            self._popolarita[a[0]] = a[1]

        artisti = DAO.getAllArtist(g)
        for a in artisti:
            self._grafo.add_node(a)
            self._idMap[a.ArtistId] = a
        self.addEdgesPesati(g)

    def addEdgesPesati(self, g):
        edges = DAO.getAllEdges(g)
        for e in edges:
            n1 = self._idMap.get(e[0])
            n2 = self._idMap.get(e[1])
            if n1 is None or n2 is None:
                continue
            pop1 = self._popolarita.get(n1.ArtistId, 0)
            pop2 = self._popolarita.get(n2.ArtistId, 0)

            if pop1 > pop2:
                self._grafo.add_edge(n1, n2, weight=pop1 + pop2)
            elif pop1 < pop2:
                self._grafo.add_edge(n2, n1, weight=pop1 + pop2)
            else:  # stessa popolarita -> due archi in entrambi i versi
                self._grafo.add_edge(n1, n2, weight=pop1 + pop2)
                self._grafo.add_edge(n2, n1, weight=pop1 + pop2)