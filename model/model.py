import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}
        self._popolarita = {}

    def grafo(self):
        return self._grafo

    def getNodes(self):
        return self._grafo.nodes()

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

    def get_artista_piu_influente(self):
        if len(self._grafo.nodes()) == 0:
            return None, 0
        best = None
        best_infl = None
        for n in self._grafo.nodes():
            # influenza = peso archi USCENTI − peso archi ENTRANTI
            usciti = self._grafo.out_degree(n, weight="weight")
            entrati = self._grafo.in_degree(n, weight="weight")
            infl = usciti - entrati
            if best_infl is None or infl > best_infl:
                best_infl = infl
                best = n
        return best, best_infl

    def get_top5_archi(self):
        archi = []
        for u, v, data in self._grafo.edges(data=True):
            archi.append((u, v, data["weight"]))
        archi.sort(key=lambda x: x[2], reverse=True)  # ordine decrescente per peso
        return archi[:5]

    # in model.py
    import copy

    def cammino_peso_crescente(self, partenza):
        self._cammino_ottimo = []
        self._punteggio_ottimo = 0
        parziale = [partenza]  # partenza FISSA: niente loop
        successivi = self._calcola_successivi(parziale, float("-inf"))  # primo arco: nessun vincolo
        self._calcola_cammino_ricorsivo(parziale, successivi)
        return self._cammino_ottimo, self._punteggio_ottimo

    def _calcola_cammino_ricorsivo(self, parziale, successivi):
        if len(successivi) == 0:  # CASO BASE: vicolo cieco
            if len(parziale) > self._punteggio_ottimo:
                self._punteggio_ottimo = len(parziale)
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for (s, peso) in successivi:
                parziale.append(s)
                # il peso dell'arco appena percorso diventa il nuovo peso_prec:
                nuovi_successivi = self._calcola_successivi(parziale, peso)
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                parziale.pop()

    def _calcola_successivi(self, parziale, peso_prec):
        ultimo = parziale[-1]
        ammissibili = []
        for s in self._grafo.neighbors(ultimo):
            peso = self._grafo.get_edge_data(ultimo, s)["weight"]
            if s not in parziale and peso > peso_prec:  # <-- filtro sull'ARCO + cammino semplice
                ammissibili.append((s, peso))  # ritorno anche il peso!
        return ammissibili