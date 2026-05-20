import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._popolarita = {}
        self._idMap = {}
        self._bestPath = []
        self._bestObjVal = 0

    def getBestPath(self, v0):
        self._bestPath = [v0]
        self._bestObjVal = 1

        parziale = [v0]

        for v in self._grafo.successors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath

    def _ricorsione(self, parziale):
        #ottimalità
        if len(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = len(parziale)

        #terminazione

        #ricorsione
        for v in self._grafo.successors(parziale[-1]):
            pesoNuovo = self._grafo[parziale[-1]][v]["weight"]
            pesoVecchio = self._grafo[parziale[-2]][parziale[-1]]["weight"]
            if pesoNuovo > pesoVecchio and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()


    def getAllGenre(self):
        return DAO.getAllGenre()

    def getAllArtists(self, genere):
        artisti = DAO.getAllArtists(genere)
        self._idMap = {}
        for a in artisti:
            self._idMap[a.Name] = a
        return artisti

    def creaGrafo(self, genere):
        artisti = DAO.getAllArtists(genere)
        self._idMap = {}
        for a in artisti:
            self._idMap[a.Name] = a

        self._grafo.clear()
        self._grafo.add_nodes_from(artisti)

        self._popolarita = DAO.getPopolaritaArtisti(genere)

        clientiArtista = {}
        for ar in artisti:
            clientiArtista[ar] = DAO.getClientiArtista(ar.ArtistId, genere)

        #creazione archi
        for i in range(len(artisti)):
            for j in range(i+1, len(artisti)):
                a = artisti[i]
                b = artisti[j]

                clientiA = clientiArtista.get(a, set())
                clientiB = clientiArtista.get(b, set())

                comuni = clientiA.intersection(clientiB)
                #se hanno almeno un cliente in comune
                if len(comuni) > 0:
                    popA = self._popolarita.get(a, 0) #se chiave non c'è, mai comprato, restiruisce 0
                    popB = self._popolarita.get(b, 0)

                    peso = popA + popB

                    #direzione arco
                    if popA > popB:
                        self._grafo.add_edge(a, b, weight=peso)
                    elif popB > popA:
                        self._grafo.add_edge(b, a, weight=peso)
                    else: #se pop uguale 2 archi di verso opposto
                        self._grafo.add_edge(a, b, weight=peso)
                        self._grafo.add_edge(b, a, weight=peso)


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getBestArtist(self):
        bestArtist = None
        maxInfluenza = -1

        for nodo in self._grafo.nodes:
            pesoEdegesUscenti = 0
            for a, b, p in self._grafo.out_edges(nodo, data=True): #arco dato come (a, b, {'weight':50})
                pesoEdegesUscenti += p["weight"]

            pesoEdgesEntranti = 0
            for a, b, p in self._grafo.in_edges(nodo, data=True):
                pesoEdgesEntranti += p["weight"]

            influenza = pesoEdegesUscenti - pesoEdgesEntranti

            if influenza > maxInfluenza:
                maxInfluenza = influenza
                bestArtist = nodo

        return bestArtist, maxInfluenza

    def getTopEdges(self):
        archiOrdinati = sorted(self._grafo.edges(data=True),
                               key=lambda x: x[2]["weight"],
                               reverse=True) #crea lista ordinata, originale non viene toccato
        return archiOrdinati[:5] #primi 5