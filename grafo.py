#!/usr/bin/python
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""
from random import random

class Grafo:
    """ Representa un grafo no dirigido pesado """

    def __init__(self, inv_arista = None):
        self.adyacencias = {}
        self.inv_arista = inv_arista

    def __str__(self):
        """ Para pruebas """
        return str(self.adyacencias)

    def __iter__(self):
        return iter(self.adyacencias)

    def _pertenecen(self, vertice_a, vertice_b):
        return vertice_a in self.adyacencias and \
            vertice_b in self.adyacencias

    def agregar_vertice(self, vertice):
        if vertice not in self.adyacencias:
            self.adyacencias[vertice] = {}

    def sacar_vertice(self, vertice):
        if vertice not in self.adyacencias: return
        for v in self.adyacencias.keys():
            if not self.estan_conectados(v, vertice): continue
            sacar_arista(self, v, vertice)

        self.adyacencias.pop(vertice)

    def agregar_arista(self, vertice_i, vertice_j, costo):
        if not self._pertenecen(vertice_i, vertice_j): return

        self.adyacencias[vertice_i][vertice_j] = costo
        costo_j = costo
        if self.inv_arista:
            costo_j = self.inv_arista(costo)
        self.adyacencias[vertice_j][vertice_i] = costo_j


    def sacar_arista(self, vertice_i, vertice_j):
        if not self._pertenecen(vertice_i, vertice_j): return
        self.adyacencias[vertice_i].pop(vertice_j)
        self.adyacencias[vertice_j].pop(vertice_i)



    def estan_conectados(self, vertice_i, vertice_j):
        return self._pertenecen(vertice_i, vertice_j) and \
            vertice_j in self.adyacencias[vertice_i]

    def adyacentes(self, vertice):
        if vertice not in self.adyacencias: return
        return self.adyacencias[vertice].keys()

    def peso(self, vertice_i, vertice_j):
        if not self.estan_conectados(vertice_i, vertice_j): return
        return self.adyacencias[vertice_i][vertice_j]

    def obtener_vertice(self):
        return random(self.adyacencias.keys())

    def matriz_adyacencia(self):
        """ Devuelve la matriz de adyacencia del grafo
        sin peso """

        matriz = []
        cant_v = len(self.adyacencias.keys())
        indice = {}
        i = 0
        for v in self.adyacencias.keys():
            matriz.append([0] * cant_v)
            indice[v] = i
            i += 1

        for v in self.adyacencias.keys():
            i = indice[v]
            for a in self.adyacencias[v].keys():
                j = indice[a]
                matriz[i][j] = 1
        return matriz
