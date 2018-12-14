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
import random
ORIGEN = 0
DESTINO = 1
CANTIDAD_DE_RECORRIDOS = 100
LARGO_RECORRIDO = 100
FRECUENCIA = 2

def vertice_aleatorio(pesos):
    #Pesos es un diccionario de pesos, clave vértice vecino, valor el peso.
    total = sum(pesos.values())
    rand = random.uniform(0, total)
    acum = 0
    for vertice, peso_arista in pesos.items():
        peso = peso_arista
        if acum + peso >= rand:
            return vertice
        acum += peso

def obtener_pesos_vecinos(grafo, origen, vecinos):
	return { vecino : int(grafo.peso(origen, vecino)[FRECUENCIA]) for vecino in vecinos }

def cmpFuncMax(a, b, extra):
    return b - a

def centralidad_aprox(grafo, n):
    visitados = {}
    q = Heap(cmpFuncMax)
    for _ in range(CANTIDAD_DE_RECORRIDOS):
        pesos = {}
        origen = grafo.obtener_vertice()
        visitados[origen] = 1
        for i in range(LARGO_RECORRIDO):
            vecinos = grafo.adyacentes(origen)
            pesos = obtener_pesos_vecinos(grafo, origen, vecinos)
            vecino = vertice_aleatorio(pesos)
            if(vecino not in visitados): visitados[vecino] = 1
            else: visitados[vecino] += 1
            q.encolar(vecino, pesos[vecino])
            origen = vecino

    vertices_centrales = []
    for _ in range(n + 1):
        vertices_centrales.insert(0, q.desencolar())
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
        if v == destino: return reconstruir_camino(grafo, origen, destino, padres)
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
    for v in grafo: cent[v] = (0, 0)
    for v in grafo:
        padre_dijk, distancia_dijk = ___camino_minimo(grafo, v, FRECUENCIA)
        padre_bfs, distancia_bfs = bfs(grafo, v)

        cent_aux_d = {}
        cent_aux_b = {}
        for w in grafo:
            cent_aux_d[w] = 0
            cent_aux_b[w] = 0

        vertices_ordenados_d = list(distancia_dijk.items())
        vertices_ordenados_b = list(distancia_bfs.items())

        vertices_ordenados_d.sort(key = lambda x: x[1])
        vertices_ordenados_b.sort(key = lambda x: x[1])
        # Elimino los elementos infinitos.
        vertices_ordenados_d = [v[0] for v in vertices_ordenados_d if v[1] < inf]
        for w in vertices_ordenados_d:
            if w == v: continue
            cent_aux_d[padre_dijk[w]] += 1
            cent_aux_d[padre_dijk[w]] += cent_aux_d[w]

        for w, _ in vertices_ordenados_b:
            if w == v: continue
            cent_aux_b[padre_bfs[w]] += 1
            cent_aux_b[padre_bfs[w]] += cent_aux_b[w]

        for w in grafo:
            if w == v: continue
            nuevo = (cent_aux_b[w], cent_aux_d[w])
            cent[w] = suma_tuplas(cent[w], nuevo)
    return cent

def suma_tuplas(tupla_a, tupla_b):
    return tuple(map(sum, zip(tupla_a, tupla_b)))

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
        # if v == destino: return f_reconstruir(grafo, origen, destino, padre)
        for w in grafo.adyacentes(v):
            alt = dist[v] + int(grafo.peso(v, w)[parametro])

            if alt < dist[w]:
                dist[w] = alt
                padre[w] = v
                q.encolar(w, dist[w])

    if destino: return f_reconstruir(grafo, origen, destino, padre)

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
    if not origen in grafo: return
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

def cmpTupla(a, b, extra):
    return int(a[extra]) - int(b[extra])

def prim(grafo, parametro = 0):
    vertice = grafo.obtener_vertice()
    visitados = set()
    visitados.add(vertice)
    q = Heap(cmpTupla, parametro)
    for w in grafo.adyacentes(vertice):
        q.encolar((vertice, w), grafo.peso(vertice, w))

    arbol = Grafo()
    arbol.agregar_vertices(grafo.obtener_vertices())
    while not q.esta_vacio():
        (v, w) = q.desencolar()
        if w in visitados: continue
        arbol.agregar_arista(v, w, grafo.peso(v, w))
        visitados.add(w)
        for x in grafo.adyacentes(w):
            if x not in visitados:
                q.encolar((w, x), grafo.peso(w, x))
    return arbol


def orden_topologico(grafo):
    grados = {}
    for v in grafo: grados[v] = 0
    for v in grafo:
        for w in grafo.adyacentes(v):
            grados[w] += 1
    q = Cola()
    for v in grafo:
        if grados[v] == 0: q.encolar(v)

    resultado = []
    while not q.esta_vacia():
        v = q.desencolar()
        resultado.append(v)
        for w in grafo.adyacentes(v):
            grados[w] -= 1
            if grados[w] == 0: q.encolar(w)

    return resultado



def grafo_to_file(grafo, file):
    with open(file, "w") as f:
        for v in grafo:
            for w in grafo.adyacentes(v):
                arista = ",".join([v, w] + list(grafo.peso(v, w))) + "\n"
                f.write(arista)
