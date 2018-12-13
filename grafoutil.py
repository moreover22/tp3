#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""
from grafo import *
from math import inf
from tda import Heap, Cola, Pila

ORIGEN = 0
DESTINO = 1
CANTIDAD_DE_RECORRIDOS = 10
LARGO_RECORRIDO = 20


def vertice_aleatorio(pesos):
    #Pesos es un diccionario de pesos, clave vértice vecino, valor el peso.
    total = sum(pesos.values())
    rand = random.uniform(0, total)
    acum = 0
    for vertice, peso_arista in pesos.items():
        if acum + peso_arista >= rand:
            return vertice
        acum += peso_arista

def obtener_pesos_vecinos(grafo, origen, vecinos):
	return { vecino : grafo.peso(origen, vecino) for vecino in vecinos }


def centralidad_aprox(grafo, n):
	for _ in range(0, CANTIDAD_DE_RECORRIDOS):
		origen = grafo.obtener_vertice();
		visitados = {}
		pesos = {}
		visitados[origen] = 1
		q = Heap()
		for i in range(0, LARGO_RECORRIDO):
			vecinos = grafo.adyacentes(origen)
			pesos = obtener_pesos_vecinos(grafo, origen, vecinos)
			vecino = vertice_aleatorio(pesos)
			if(vecino not in visitados): visitados[vecino] = 1
			else: visitados[vecino] += 1
			q.encolar((vecino, pesos[vecino]))
			origen = vecino
		vertices_centrales = []
		for _ in range(0, n):
			vertices_centrales.append(q.desencolar())
	return vertices_centrales

def recorrer_n_vertices(grafo, origen, n):
    """ Dado un grafo y un vertice de origen, la función de vuelve
    un recorrido desde el origen hasta el origen pasando por n ciudades
    de por medio.
    Devuelve una tupla de la forma (último, padres)
    donde último es el último vertice hasta volver a origen y padres
    es un diccionario donde se marca el recorrido.
    """
    visitados = set()
    dist = {}
    padres = {}
    dist[origen] = 0
    padres[origen] = None
    s = Pila()
    s.apilar(origen)
    ultimo = dfs(grafo, origen, visitados, padres, dist, origen, n)
    return ultimo, padres

def dfs(grafo, v, visitados, padres, dist, origen = None, nivel = inf):
    """ Almacena en padres el recorrido dfs del grafo y devuelve el último
    vertice recorrido hasta llegar a origen.
    Opcionalmente se puede determinar un nivel, el cual indicará
    la profundidad del recorrido.
     """
    if dist[v] > nivel: return
    r = None
    visitados.add(v)
    for w in grafo.adyacentes(v):
        if w == origen and dist[v] == nivel: return v
        if w in visitados: continue
        padres[w] = v
        dist[w] = dist[v] + 1
        r = dfs(grafo, w, visitados, padres, dist, origen, nivel)
        if r: return r
    visitados.remove(v)
    padres.pop(v)
    dist.pop(v)
    return r

def reconstruir_camino(grafo, origen, destino, padres, vuelve = False):
    """ Dado un grafo de ciudades, y un diccionario de padres,
    la función reconstruye el camino desde el origen hasta el destino,
    mostrando los aeropuertos que recorre. Opcionalmente si el
    recorrido es cerrado, con el parametro vuelve, muestra el ultimo
    aeropuerto de vuelta. """
    camino = []
    v = destino

    if vuelve:
        camino.append(grafo.peso(destino, origen)[DESTINO])
    peso = grafo.peso(padres[v], v)
    camino.append(peso[DESTINO])
    while peso:
        camino.append(peso[ORIGEN])
        v = padres[v]
        peso = grafo.peso(padres[v], v)
    camino.reverse()
    return camino


def bfs(grafo, origen, destino = None):
    visitados = set()
    padres = {}
    orden = {}
    q = Cola()
    visitados.add(origen)
    padres[origen] = None
    orden[origen] = 0
    q.encolar(origen)
    while not q.esta_vacia():
        v = q.desencolar()
        if v == destino:
            break
        for w in grafo.adyacentes(v):
            if w in visitados:
                 continue
            visitados.add(w)
            padres[w] = v
            orden[w] = orden[v] + 1
            q.encolar(w)
    return padres, orden


def centralidad(grafo):
    """ Devuelve un diccionario donde las claves son
    los vertices del grafo y los valores son su centralidad. """
    cent = {}
    for v in grafo: cent[v] = 0
    for v in grafo:
        padre, distancia = bfs(grafo, v)
        cent_aux = {}
        for w in grafo: cent_aux[w] = 0

        vertices_ordenados = list(distancia.items())
        vertices_ordenados.sort(key = lambda x: x[1])

        for w, _ in vertices_ordenados:
            if w == v: continue
            cent_aux[padre[w]] += 1 + cent_aux[w]

        for w in grafo:
            if w == v: continue
            cent[w] += cent_aux[w]
    return cent

def camino_minimo(grafo, origen, parametro = 0, destino = None, f_reconstruir = None):
    dist = {}
    padre = {}
    for v in grafo: dist[v] = inf
    dist[origen] = 0
    padre[origen] = None
    q = Heap()
    q.encolar(origen, dist[origen])
    while not q.esta_vacio():
        v = q.desencolar()
        if v == destino: return f_reconstruir(grafo, origen, destino, padre)
        print(v, grafo.adyacentes(v))
        for w in grafo.adyacentes(v):
            alt = dist[v] + int(grafo.peso(v, w)[parametro])

            if alt < dist[w]:
                dist[w] = alt
                padre[w] = v
                q.encolar(w, dist[w])

    # if destino: return f_reconstruir(grafo, origen, destino, padre)

    return padre, dist


def _camino_minimo(grafo, origen, parametro = 0, destino = None, f_reconstruir = None):
    dist = {}
    padre = {}
    visitados = set()

    q = Heap()
    llego = False
    for v in grafo: dist[v] = inf

    padre[origen] = None
    dist[origen] = 0

    q.encolar(origen, dist[origen])
    visitados.add(origen)
    while not q.esta_vacio():
        v = q.desencolar()
        visitados.remove(v)
        if v == destino:
            llego = True
            break
        for w in grafo.adyacentes(v):
            alt = dist[v] + int(grafo.peso(v, w)[parametro])
            if alt < dist[w]:
                dist[w] = alt
                padre[w] = v
                if not w in visitados:
                    q.encolar(w, alt)
                    visitados.add(w)
    if llego: return f_reconstruir(grafo, origen, destino, padre)
    return padre, dist

def ___camino_minimo(grafo, origen, parametro = 0, destino = None, f_reconstruir = None):
    visitados = set()
    dist = {}
    padre
    for v in grafo:
        pass
