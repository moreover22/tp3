#!/usr/bin/python
from random import random
class Grafo:
    def __init__(self):
        self.adyacencias = {}

    def agregar_vertice(self, vertice):
        """ vertice = (clave, datos)... No sé... """
        if vertice not in self.adyacencias:
            self.adyacencias[vertice] = {}

    # Hay que hacerlo dirigido o no dirigido?
    def sacar_vertice(self, vertice):
        if vertice not in self.adyacencias:
            return
        for v in self.adyacencias.keys():
            if not estan_conectados(self, v, vertice):
                continue
            sacar_arista(self, v, vertice)

        self.adyacencias.pop(vertice)

    # Hay que hacerlo dirigido o no dirigido?
    def agregar_arista(self, vertice_orig, vertice_dest, costo):
        if vertice_orig not in self.adyacencias:
            return
        self.adyacencias[vertice_orig][vertice_dest] = costo


    def sacar_arista(self, vertice_orig, vertice_dest):
        if vertice_orig not in self.adyacencias:
            return
        return self.adyacencias[vertice_orig].pop(vertice_dest)

    # Hay que hacerlo dirigido o no dirigido?
    def estan_conectados(self, vertice_orig, vertice_dest):
        return vertice_orig in self.adyacencias and \
            vertice_dest in self.adyacencias[vertice_orig]

    def adyacentes(self, vertice):
        if vertice not in self.adyacencias:
            return
        return self.adyacencias[vertive]

    def peso(self, vertice_orig, vertice_dest):
        if not estan_conectados(self, vertice_orig, vertice_dest)
            return
        return self.adyacencias[vertice_orig][vertice_dest]
    def obtener_vertice(self):
        return random(self.adyacencias.keys())
