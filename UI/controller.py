import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.getGenres()
        for g in generi:
            self._view._ddGenre.options.append(ft.dropdown.Option(key=g.GenreId, text=g.Name)
            )
        self._view.update_page()

    def handleCreaGrafo(self, e):
        if self._view._ddGenre.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserisci un genere.", color="red"))
            self._view.update_page()
            return

        self._model.buildGrafo(self._view._ddGenre.value)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.get_numnodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.get_numarchi()}"))
        self._view.update_page()

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass