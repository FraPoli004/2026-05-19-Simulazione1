import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodi = []
        self._idMap = {}

    def getGenres(self):
        return DAO.getAllGenres()

    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    def buildGraph(self,g):
        self._grafo.clear()
        artisti = DAO.getAllArtist(g)
        for a in artisti:
            self._grafo.add_node(a)
            self._idMap[a.ArtistId]= a
        #self._grafo.addEdgesPesati()


