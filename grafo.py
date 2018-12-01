#!/usr/bin/python
from random import random

class Grafo:
    """ Representa un grafo no dirigido pesado """

    def __init__(self):
        self.adyacencias = {}

    def _pertenecen(self, vertice_a, vertice_b):
        return vertice_a in self.adyacencias and \
            vertice_b in self.adyacencias:

    def agregar_vertice(self, vertice):
        """ vertice = (clave, datos)... No sé... """
        if vertice not in self.adyacencias:
            self.adyacencias[vertice] = {}

    def sacar_vertice(self, vertice):
        if vertice not in self.adyacencias:
            return
        for v in self.adyacencias.keys():
            if not estan_conectados(self, v, vertice):
                continue
            sacar_arista(self, v, vertice)

        self.adyacencias.pop(vertice)

    def agregar_arista(self, vertice_orig, vertice_dest, costo):
        if not _pertenecen(self, vertice_orig, vertice_dest):
            return
        self.adyacencias[vertice_orig][vertice_dest] = costo
        self.adyacencias[vertice_dest][vertice_orig] = costo


    def sacar_arista(self, vertice_orig, vertice_dest):
        if not _pertenecen(self, vertice_orig, vertice_dest):
            return
        self.adyacencias[vertice_orig].pop(vertice_dest)
        self.adyacencias[vertice_dest].pop(vertice_orig)



    def estan_conectados(self, vertice_orig, vertice_dest):
        return _pertenecen(self, vertice_orig, vertice_dest) and \
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
