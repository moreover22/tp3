#!/usr/bin/python
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""

import sys
from flycombi import *
from grafo import Grafo

CANT_ARCHIVOS = 2
DELIMITADOR_CSV = ','
CIUDAD = 1
def inv_arista(costo):
    i, j, tiempo_prom, precio, cant_vuelos_entre_aeropuertos = costo
    return (j, i, tiempo_prom, precio, cant_vuelos_entre_aeropuertos)

def grafo_archivo(file_vertices, file_aristas):
    """ Dado una ruta a archivos con info de vertices y de aristas,
    genera un grafo con sus relaciones. """
    grafo = Grafo(inv_arista)
    with open(file_vertices) as vertices, \
         open(file_aristas) as aristas:

        aeropuertos = {}
        for v in vertices:
            ciudad, clave, lat, long = v.rstrip('\n').split(DELIMITADOR_CSV)
            aeropuertos[clave] = (clave, ciudad, lat, long)
            grafo.agregar_vertice(ciudad)
        for a in aristas:
            aer_i, aer_j, tiempo, precio, cant_vuelos = \
                a.rstrip('\n').split(DELIMITADOR_CSV)

            ciudad_i = aeropuertos[aer_i][CIUDAD]
            ciudad_j = aeropuertos[aer_j][CIUDAD]

            grafo.agregar_arista(ciudad_i, ciudad_j, (aer_i, aer_j, \
                tiempo, precio, cant_vuelos))
        return grafo, aeropuertos

def cargar_archivos(archivos):
    if len(archivos) > CANT_ARCHIVOS: return
    f_aeropuertos, f_vuelos = archivos
    return grafo_archivo(f_aeropuertos, f_vuelos)

def main(argv):
    """ Funcion principal """
    grafo, aeropuertos = cargar_archivos(argv)
    if not grafo: return

    # return
    # print(grafo)
    # for v in grafo:
        # print(v)
    # for w in grafo.adyacentes('Gotica'):
        # print(w)
    while(True):
        flycombi(grafo)

if __name__ == '__main__':
    main(sys.argv[1:])
