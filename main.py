#!/usr/bin/python

import sys
from flycombi import *

#Habría que cambiarlo...
def grafo_archivo(archivo):
    """ Dado un nombre de archivo, devuelve un grafo
    creado. (No sé si sirve así) """
    with open(archivo, 'r') as f:
        grafo = crear_grafo(f.read()) # Creo que no anda así ...

        return grafo

def cargar_archivos(archivos):
    grafos = [] # Creo que no sirve así...
    for archivo in archivos:
        grafos.push(grafo_archivo(archivo))
    return grafos

def main(argv):
    """ Funcion principal"""
    grafos = cargar_archivos(argv)
    flycombi() 

if __name__ == '__main__':
    main(sys.argv[1:])
