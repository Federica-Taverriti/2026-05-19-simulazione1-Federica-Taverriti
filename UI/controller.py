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

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente!", color="green")
        )
        nNodi, nArchi = self._model.getGraphDetails()

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di vertici: {nNodi} - Numero di archi: {nArchi}")
        )

        for n in self._model._grafo.nodes:
            self._view.txt_result.controls.append(
                ft.Text(f"{n.ArtistId} - {n.Name}.")
            )

        self._view.update_page()


    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass