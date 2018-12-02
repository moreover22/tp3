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
ARGS_CAMINO_MAS = 3
MODO_CAMINO_MAS = {"rapido" : 2, "barato" : 3}

def mostrar_recorrido(vuelos):
    print(str(vuelos[0]), end = "")
    for v in vuelos[1:]:
        print(" -> " + str(v), end = "")
    print()

def listar_operaciones(grafo, args):
    """ Imprime en la salida estandar los comandos disponibles
    Pre: args debe ser una lista vacía.
    """
    for comando in COMANDOS.keys():
        print(comando)

def camino_mas(grafo, args):
    if len(args) != ARGS_CAMINO_MAS: return
    modo, origen, destino = args
    mostrar_recorrido(camino_minimo(grafo, origen, MODO_CAMINO_MAS[modo],
        destino, reconstruir_camino))

def centralidad(grafo):
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


COMANDOS = {'listar_operaciones' : listar_operaciones, 
            'camino_mas' : camino_mas,
            'centralidad' : centralidad
            }

def flycombi(grafo):
    camino_mas(grafo, ["barato","Lanus", "Shelbyville"])
    print("dijkstra")
    # print(dijkstra(grafo, "Lanus", "Shelbyville"))
    # print(camino_minimo(grafo, "San Diego","New York"))
    # print(bfs(grafo, "Lanus"))
    # print(sorted(centralidad(grafo).items(), key=lambda x: x[1]))
    # print(centralidad(grafo))
    entrada = input()
    entrada = entrada.split(COMANDO_SEP);
    comando = entrada[CMD]
    # En caso de que no tenga argumentos, pasa a ser una lista vacia
    entrada = COMANDO_SEP.join(entrada[ARGS:])
    args = entrada.split(ARGS_SEP) if ARGS < len(entrada) else []
    if comando in COMANDOS:
        COMANDOS[comando](grafo, args)

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
ORIGEN = 0
DESTINO = 1
def reconstruir_camino(grafo, origen, destino, padres):
    camino = []
    v = destino
    camino.append((v, grafo.peso(v, padres[v])[ORIGEN]))
    while v != origen:
        camino.append((padres[v], grafo.peso(v, padres[v])[DESTINO]))
        v = padres[v]
    camino.reverse()
    return camino
