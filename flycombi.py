#!/usr/bin/python
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""
from tda import Heap, Cola, Pila
from math import inf
COMANDO_SEP = ' '
ARGS_SEP = ','
CMD = 0
ARGS = 1
ARGS_CAMINO_MAS = 3
MODO_CAMINO_MAS = {"rapido" : 2, "barato" : 3}
VACACIONES_ARGS = 2
ORIGEN = 0
DESTINO = 1

def mostrar_recorrido(vuelos):
    print(str(vuelos[0]), end = "")
    for v in vuelos[1:]:
        print(" -> " + str(v), end = "")

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

def vacaciones(grafo, args):
    if len(args) != VACACIONES_ARGS: return
    origen, n = args
    ultimo, padres = recorrer_n_vertices(grafo, origen, int(n))

    if not ultimo:
        print("No se encontro recorrido")
        return

    recorrido = reconstruir_camino(grafo, origen, ultimo, padres, True)
    mostrar_recorrido(recorrido)



COMANDOS = {'listar_operaciones' : listar_operaciones,
            'camino_mas' : camino_mas,
            'centralidad' : centralidad,
            'vacaciones' : vacaciones
            }

def flycombi(grafo):
    vacaciones(grafo, ["New York", "15"])
    # print(camino_mas(grafo, ["rapido","San Diego","New York"]))
    # print(grafo.matriz_adyacencia())
    # print(bfs(grafo, "Lanus"))
    # print(sorted(centralidad(grafo).items(), key=lambda x: x[1]))
    entrada = input()
    entrada = entrada.split(COMANDO_SEP);
    comando = entrada[CMD]
    # En caso que los argumentos tengan espacios
    entrada = COMANDO_SEP.join(entrada[ARGS:])
    # En caso de que no tenga argumentos, pasa a ser una lista vacia
    args = entrada.split(ARGS_SEP) if ARGS < len(entrada) else []
    if comando in COMANDOS:
        COMANDOS[comando](grafo, args)
    print()

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

def reconstruir_camino(grafo, origen, destino, padres, vuelve = False):
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

def recorrer_n_vertices(grafo, origen, n):
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
    if dist[v] > nivel: return
    r = None
    visitados.add(v)
    for w in grafo.adyacentes(v):
        # print(w + " " + origen)
        if w == origen: return v # and dist[v] == nivel: return v
        if w in visitados: continue
        padres[w] = v
        dist[w] = dist[v] + 1
        r = dfs(grafo, w, visitados, padres, dist, origen, nivel)
        if r: return r
    visitados.remove(v)
    padres.pop(v)
    dist.pop(v)
    return r
