import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._artisti = []
        self._popolarita = {}

    def getAllGenre(self):
        return DAO.getAllGenre()

    def creaGrafo(self, genere):
        self._artisti = DAO.getAllArtists(genere)
        self._grafo.clear()
        self._grafo.add_nodes_from(self._artisti)

        self._popolarita = DAO.getPopolaritaArtisti(genere)

        clientiArtista = {}
        for ar in self._artisti:
            clientiArtista[ar] = DAO.getClientiArtista(ar.ArtistId)

        #creazione archi
        for i in range(len(self._artisti)):
            for j in range(i+1, len(self._artisti)):
                a = self._artisti[i]
                b = self._artisti[j]

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