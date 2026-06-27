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

        self._model.buildGraph(self._view._ddGenre.value)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.get_numnodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.get_numarchi()}"))
        self.fillDDArtist()
        best, influenza = self._model.get_artista_piu_influente()
        self._view.txt_result.controls.append(ft.Text(f"l'artista più influente è: {best} con influenza: {influenza}"))
        archi5 = self._model.get_top5_archi()
        self._view.txt_result.controls.append(ft.Text(f"i 5 archi di peso maggiore sono:"))
        for a in archi5:
            self._view.txt_result.controls.append(
                ft.Text(f"{a[0]}------>{a[1]}, peso: {a[2]}"))


        self._view.update_page()

    def fillDDArtist(self):
        artisti = self._model.getNodes()
        for a in artisti:
            self._view._ddArtist.options.append(ft.dropdown.Option(key=a.ArtistId, text=a.Name)
                                               )
        self._view.update_page()


    def handleCammino(self,e):
        if not self._model.getNodes():
            self._view.create_alert("Crea prima il grafo!");
            self._view.update_page()
            return
        if self._view._ddArtist.value is None:  # <-- ADATTA al nome del dropdown
            self._view.create_alert("Seleziona un artista di partenza!")
            self._view.update_page()
            return

        partenza = self._model._idMap[int(self._view._ddArtist.value)]
        cammino, lunghezza = self._model.cammino_peso_crescente(partenza)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"il cammino è lungo: {lunghezza}"))
        for n in cammino:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()