import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.getAllGenre()

        generiDD = list(map(lambda x: ft.dropdown.Option(x), generi))
        self._view._ddGenre.options = generiDD
        self._view.update_page()

    def handleCreaGrafo(self, e):
        genere = self._view._ddGenre.value
        if genere is None:
            self._view.create_alert("Selezionare un genere.")
            return
        self._model.creaGrafo(genere)

        self.fillDDArtist()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente!", color="green")
        )
        nNodi, nArchi = self._model.getGraphDetails()

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di vertici: {nNodi} - Numero di archi: {nArchi}")
        )

        bestArtist, influenza = self._model.getBestArtist()

        self._view.txt_result.controls.append(
            ft.Text(f"Artista con maggiore influenza: {bestArtist} ({influenza})", color="purple")
        )

        topEdges = self._model.getTopEdges()
        self._view.txt_result.controls.append(
            ft.Text("Top 5 archi:", color="blue")
        )

        for a, b, p in topEdges:
            self._view.txt_result.controls.append(
                ft.Text(f"{a} -> {b} (Acquisti/peso: {p['weight']})", color="blue")
            )

        self._view.update_page()


    #def handleCreaGrafo(self,e):
        #pass

    def fillDDArtist(self):
        genere = self._view._ddGenre.value
        artisti = self._model.getAllArtists(genere)

        artistiDD = list(map(lambda x: ft.dropdown.Option(x), artisti))
        self._view._ddArtist.options = artistiDD
        self._view.update_page()

    def handleCammino(self,e):
        pass