#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""
from grafoutil import *

DELIMITADOR_CSV = ','
ARGS_SEP = ','
COMANDO_SEP = ' '
CMD = 0
ARGS = 1
ARGS_CAMINO_MAS = 3
MODO_CAMINO_MAS = {"rapido" : 2, "barato" : 3}
ARGS_CAMINO_ESCALAS = 2
VACACIONES_ARGS = 2
ORIGEN = 0
DESTINO = 1
CANT_ARCHIVOS = 2
CIUDAD = 1
CETRALIDAD_ARGS = 1
CENTRALIDAD_APROX_ARGS = 1

def inv_arista(costo):
    i, j, tiempo_prom, precio, cant_vuelos_entre_aeropuertos = costo
    return (j, i, tiempo_prom, precio, cant_vuelos_entre_aeropuertos)

def mostrar_recorrido(vuelos):
    """ Dado una lista de vuelos, muestra en pantalla la secuencia del vuelo """
    if not vuelos: return
    # print(vuelos)
    print(" -> ". join(vuelos))

def listar_operaciones(flyCombi, args):
    """ Imprime en la salida estandar los comandos disponibles
    Pre: args debe ser una lista vacía.
    """
    for comando in COMANDOS.keys():
        if comando == 'listar_operaciones': continue
        print(comando)

def camino_mas(flyCombi, args):
    """ Dado un grafo ya inicializado y la lista args con los siguientes
    elementos:
    * modo: rapido|barato
    * origen: ciudad de origen
    * destino: ciudad de destino
    Muestra en pantalla el recorrido más rapido/barato
    desde la ciudad origen hasta destino. """
    if len(args) != ARGS_CAMINO_MAS: return
    grafo = flyCombi.get_grafo_ciudades()
    modo, origen, destino = args
    mostrar_recorrido(camino_minimo(grafo, origen, MODO_CAMINO_MAS[modo],
        destino, reconstruir_camino))

def camino_escalas(grafo,args):
	if len(args) != ARGS_CAMINO_MAS: return
	origen, destino = args
	padres,orden = bfs(grafo,origen,destino)
	mostrar_recorrido(reconstruir_camino(grafo,origen,destino,padres))

def vacaciones(flyCombi, args):
    """ Dado un grafo ya inicializado y la lista args con los siguientes
    elementos:
    * origen: ciudad de origen
    * k: cantidad de ciudades intermedias
    Muestra en pantalla el recorrido desde la ciudad de origen a k ciudades
    volviendo a la ciudad de origen. """

    return
    if len(args) != VACACIONES_ARGS: return
    grafo = flyCombi.get_grafo_ciudades()
    origen, n = args
    ultimo, padres = recorrer_n_vertices(grafo, origen, int(n))
    if not ultimo:
        print("No se encontro recorrido")
        return
    recorrido = reconstruir_camino(grafo, origen, ultimo, padres, True)
    mostrar_recorrido(recorrido)




def _centralidad(flyCombi, args):
    if len(args) != CETRALIDAD_ARGS: return
    grafo = flyCombi.get_grafo_aeropuertos()
    n = int(args[0])
    q = Heap()
    cent = centralidad(grafo).items()
    cont = 0
    for vertice, centr in cent:
        q.encolar(vertice, centr)
        cont += 1
        if(cont > n):
            q.desencolar()
    resultado = []
    for i in range(n):
        resultado.insert(0, q.desencolar())
    print(", ".join(resultado))

def _centralidad_aprox(flyCombi, args):
    if len(args) != CENTRALIDAD_APROX_ARGS: return
    n = int(args[0])
    grafo = flyCombi.get_grafo_aeropuertos()
    cent_aprox = centralidad_aprox(grafo, n)
    print(", ".join(cent_aprox))


COMANDOS = {'listar_operaciones' : listar_operaciones,
            'camino_mas' : camino_mas,
            'centralidad' : _centralidad,
            # 'centralidad_aprox' : _centralidad_aprox,
            'vacaciones' : vacaciones
            }

def flycombi(flyCombi):
    # vacaciones(grafo, ["New York", "15"])
    # print(camino_mas(grafo, ["rapido","San Diego","New York"]))
    # print(grafo.matriz_adyacencia())
    # print(bfs(grafo, "Lanus"))
    # print(sorted(centralidad(grafo).items(), key=lambda x: x[1]))
    # print(grafo)
    try:
        entrada = input()
    except EOFError:
        return None
    entrada = entrada.split(COMANDO_SEP);
    comando = entrada[CMD]
    # En caso que los argumentos tengan espacios
    entrada = COMANDO_SEP.join(entrada[ARGS:])
    # En caso de que no tenga argumentos, pasa a ser una lista vacia
    args = entrada.split(ARGS_SEP) if ARGS <= len(entrada) else []
    if comando in COMANDOS:
        COMANDOS[comando](flyCombi, args)
    # print()
    return True


class FlyCombi:

    def __init__(self):
        self.grafo_ciudades = Grafo(False, inv_arista)
        self.grafo_aeropuertos = Grafo(True)
        self.aeropuertos = {}

    def get_grafo_ciudades(self):
        return self.grafo_ciudades
    def get_grafo_aeropuertos(self):
        return self.grafo_aeropuertos
    def get_aeropuertos(self):
        return self.aeropuertos

    def cargar_archivos(self, archivos):
        """ Dada una lista con rutas de archivos:
        * ruta_aeropuertos
        * ruta_vuelos
        Asigna un grafo con ciudades como vertices
        y vuelos como aristas, un grafo con aeropuertos
        como vertices y vuelos como aristas, un diccionario
        con info de aeropuertos. """

        if len(archivos) != CANT_ARCHIVOS: return
        file_vertices, file_aristas = archivos
        with open(file_vertices) as vertices, \
             open(file_aristas) as aristas:

            for v in vertices:
                ciudad, clave, lat, long = v.rstrip('\n').split(DELIMITADOR_CSV)
                self.aeropuertos[clave] = (clave, ciudad, lat, long)
                self.grafo_aeropuertos.agregar_vertice(clave)
                self.grafo_ciudades.agregar_vertice(ciudad)
            for a in aristas:
                aer_i, aer_j, tiempo, precio, cant_vuelos = \
                    a.rstrip('\n').split(DELIMITADOR_CSV)

                ciudad_i = self.aeropuertos[aer_i][CIUDAD]
                ciudad_j = self.aeropuertos[aer_j][CIUDAD]

                self.grafo_aeropuertos.agregar_arista(aer_i, aer_j, (tiempo, \
                precio, cant_vuelos))

                self.grafo_ciudades.agregar_arista(ciudad_i, ciudad_j, \
                (aer_i, aer_j, tiempo, precio, cant_vuelos))
