#!/usr/bin/python
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""

import sys
from flycombi import *

def main(argv):
    """ Funcion principal """
    grafo, aeropuertos = cargar_archivos(argv)
    if not grafo: return
    while(True):
        flycombi(grafo)

if __name__ == '__main__':
    main(sys.argv[1:])
