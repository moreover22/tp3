#!/usr/bin/python
class Grafo:
    def __init__(self):
        self.adyacencias = {}

    def agregar_vertice(self, vertice):
        """ vertice = (clave, datos)... No sé... """
        if vertice not in self.adyacencias:
            self.adyacencias[vertice] = {}

    # Hay que hacerlo dirigido o no dirigido?
    def sacar_vertice(self, vertice):
        if vertice not in self.adyacentes:
            return
        for v in self.adyacentes.keys():
            if not estan_conectados(self, v, vertice):
                continue
            sacar_arista(self, v, vertice)

        self.adyacentes.pop(vertice)

    # Hay que hacerlo dirigido o no dirigido?
    def agregar_arista(self, vertice_orig, vertice_dest, costo):
        if vertice_orig not in self.adyacentes:
            return
        self.adyacentes[vertice_orig][vertice_dest] = costo


    def sacar_arista(self, vertice_orig, vertice_dest):
        if vertice_orig not in self.adyacentes:
            return
        return self.adyacentes[vertice_orig].pop(vertice_dest)

    # Hay que hacerlo dirigido o no dirigido?
    def estan_conectados(self, vertice_orig, vertice_dest):
        return vertice_orig in self.adyacentes and \
            vertice_dest in self.adyacentes[vertice_orig]

    def adyacentes(self, vertice):
        if vertice not in self.adyacentes:
            return
        return self.adyacentes[vertive]

    def peso(self, vertice_orig, vertice_dest):
        if not estan_conectados(self, vertice_orig, vertice_dest)
            return
        return self.adyacentes[vertice_orig][vertice_dest]
