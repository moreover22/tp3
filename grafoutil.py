#!/usr/bin/python
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

def centralidad(grafo):
    """ Devuelve un diccionario donde las claves son
    los vertices del grafo y los valores son su centralidad. """
    cent = {}
    for v in grafo: cent[v] = 0
    for v in grafo:
        for w in grafo:
            if v == w: continue
            padre, distancia = bfs(grafo, v, w)
            if w not in padre: continue
            actual = padre[w]

            while actual != v:
                cent[actual] += 1
                actual = padre[actual]
    return cent

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
    """ Dado un  """
    camino = []
    v = destino
    if vuelve:
        camino.append(grafo.peso(destino, origen)[DESTINO])

    camino.append(grafo.peso(v, padres[v])[ORIGEN])
    while v != origen:
        camino.append(grafo.peso(v, padres[v])[DESTINO])
        v = padres[v]
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

def camino_minimo(grafo, origen, parametro = 0, destino = None, f_reconstruir = None):
    dist = {}
    padre = {}

    dist[origen] = 0
    q = Heap()

    for v in grafo:
        if v != origen:
            dist[v] = inf
        padre[v] = None
        q.encolar(v, dist[v])

    while not q.esta_vacio():
        v = q.desencolar()
        for w in grafo.adyacentes(v):
            alt = dist[v] + int(grafo.peso(v, w)[parametro])
            if alt < dist[w]:
                dist[w] = alt
                padre[w] = v
    if destino: return f_reconstruir(grafo, origen, destino, padre)
    return padre, dist
