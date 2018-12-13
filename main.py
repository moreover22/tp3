#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""

import sys
from flycombi import *

def main(argv):
    """ Funcion principal """
    fc = FlyCombi()
    fc.cargar_archivos(argv)
    while(True):
        if not flycombi(fc):
            break

if __name__ == '__main__':
    main(sys.argv[1:])
