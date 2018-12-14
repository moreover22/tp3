#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""
from random import random, choice

class Grafo:
    """
    Representa un grafo. El mismo puede ser pesado o no, dirigido o no.
    Cuenta con las primitivas de agregar, sacar vertices y aristas, adyacentes
    a un vertice, peso de arista (si es pesado), obtener vertice.
    """

    def __init__(self, dirigido = False, inv_arista = None):
        """ Inicializa un grafo, dirigido indica si el grafo va a ser dirigido
        o no. inv_arista es una función que sirve para crear el peso de j a i
        (siendo i y j dos vertices)
        """
        self.adyacencias = {}
        self.inv_arista = inv_arista
        self.dirigido = dirigido

    def __str__(self):
        """ Devuelve el grafo como un string"""
        return str(self.adyacencias)

    def __iter__(self):
        """ Devuelve el grafo como una estructura iterable """
        return iter(self.adyacencias)

    def _pertenecen(self, vertice_a, vertice_b):
        """ Devuelve True vertice_a y vertice_b pertenecen al grafo """
        return vertice_a in self.adyacencias and \
            vertice_b in self.adyacencias

    def agregar_vertice(self, vertice):
        """ Agrega un vertice al grafo. """
        if vertice not in self.adyacencias:
            self.adyacencias[vertice] = {}

    def sacar_vertice(self, vertice):
        """ Elimina un vertice del grafo. Además borra todas las
        aristas relacionadas con el vertice. """
        if vertice not in self.adyacencias: return
        for v in self.adyacencias.keys():
            if not self.estan_conectados(v, vertice): continue
            sacar_arista(self, v, vertice)
        self.adyacencias.pop(vertice)

    def agregar_arista(self, vertice_i, vertice_j, costo = 1):
        """ Agrega una arista entre el vertice_i y el vertice_j.
        Opcionalmente se puede asignar un costo si el grafo es pesado.
        Si alguno de los dos vertices no existen, la función no hace nada.
        """
        if not self._pertenecen(vertice_i, vertice_j): return

        self.adyacencias[vertice_i][vertice_j] = costo
        if self.dirigido: return
        costo_j = costo
        if self.inv_arista:
            costo_j = self.inv_arista(costo)
        self.adyacencias[vertice_j][vertice_i] = costo_j


    def sacar_arista(self, vertice_i, vertice_j):
        """ Elimina la arista (vertice_i, vertice_j) (si es dirigido, si no,
        también elimina (vertice_j, vertice_i)). Se espera que ambos vertices
        existan.
        """
        if not self._pertenecen(vertice_i, vertice_j): return
        self.adyacencias[vertice_i].pop(vertice_j)
        if self.dirigido:
            self.adyacencias[vertice_j].pop(vertice_i)

    def estan_conectados(self, vertice_i, vertice_j):
        """ Devuelve True si vertice_i está conecta con vertice_j o viceversa """
        return self._pertenecen(vertice_i, vertice_j) and \
            (vertice_j in self.adyacencias[vertice_i] or \
             vertice_i in self.adyacencias[vertice_j])

    def adyacentes(self, vertice):
        """ Devuelve una lista con todos los vertices adyacentes al vertice.
        Se espera que el vertice exista en el grado.
        """
        if vertice not in self.adyacencias: return
        return self.adyacencias[vertice].keys()

    def peso(self, vertice_i, vertice_j):
        """ Devuelve el peso de la arista entre vertice_i y vertice_j, si el
        grafo es no pesado, devuelve 1 si están conectados. """
        if not self.estan_conectados(vertice_i, vertice_j): return
        return self.adyacencias[vertice_i][vertice_j]

    def obtener_vertice(self):
        """ Devuelve un vertice aleatorio del grafo. """
        return choice(list(self.adyacencias.keys()))

    def agregar_vertices(self, vertices):
        for v in vertices:
            self.agregar_vertice(v)
    def obtener_vertices(self):
        return list(self.adyacencias.keys())


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
