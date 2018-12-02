#!/usr/bin/python
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""
from tda import Heap, Cola
from math import inf
COMANDO_SEP = ' '
ARGS_SEP = ','
CMD = 0
ARGS = 1

def listar_operaciones(grafo, args):
    """ Imprime en la salida estandar los comandos disponibles
    Pre: args debe ser una lista vacía.
    """
    for comando in COMANDOS.keys():
        print(comando)

def camino_mas(grafo, args):
    pass

COMANDOS = { 'listar_operaciones' : listar_operaciones, 'camino_mas' : camino_mas }

def flycombi(grafo):
    print(camino_minimo(grafo, "Lanus", "Riverdale"))
    print("dijkstra")
    print(dijkstra(grafo, "Lanus")) #, "Shelbyville"))
    # print(bfs(grafo, "Lanus"))
    # print(centralidad(grafo))
    entrada = input()
    entrada = entrada.split(COMANDO_SEP);
    comando = entrada[CMD]
    # En caso de que no tenga argumentos, pasa a ser una lista vacia
    args = entrada[ARGS].split(ARGS_SEP) if ARGS < len(entrada) else []
    if comando in COMANDOS:
        COMANDOS[comando](grafo, args)


PRECIO = 2
def dijkstra(grafo, origen):
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
            alt = dist[v] + int(grafo.peso(v, w)[PRECIO])
            if alt < dist[w]:
                dist[w] = alt
                padre[w] = v
                q.encolar(v, alt)
    return padre, dist

# NO FUNCIONA,
def camino_minimo(grafo, origen, destino = None ):
    dist = {}
    padre = {}
    for v in grafo: dist[v] = inf
    dist[origen] = 0
    padre[origen] = None
    q = Heap()
    q.encolar(origen, dist[origen])
    while not q.esta_vacio():
        v = q.desencolar()
        if v == destino:
            return reconstruir_camino(origen, destino, padre)
        for w in grafo.adyacentes(v):
            print("ad " + w + " " + str(grafo.peso(v, w)))
            if dist[v] + int(grafo.peso(v, w)[PRECIO]) < dist[w]:
                dist[w] = dist[v] + int(grafo.peso(v, w)[PRECIO])
                padre[w] = v
                q.encolar(w, dist[w])

    return padre, dist ## No llego a destino

# Depende de camino_minimo
def centralidad(grafo):
    cent = {}
    for v in grafo: cent[v] = 0
    for v in grafo:
        for w in grafo:
            if v == w: continue
            padre, distancia = camino_minimo(grafo, v, w)
            if w not in padre: continue
            actual = padre[w]
            print(">>>> " + str(padre))
            while actual != v:
                cent[actual] += 1
                actual = padre[actual]
    return cent


def bfs(grafo, origen):
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
        for w in grafo.adyacentes(v):
            if w in visitados:
                continue
            visitados.add(w)
            padres[w] = v
            orden[w] = orden[v] + 1
            q.encolar(w)
    return padres, orden

def reconstruir_camino(origen, destino, padres):
    camino = []
    v = destino
    while v != origen:
        camino.append(v)
        v = padres[v]
    camino.append(origen)
    camino.reverse()
    return camino
