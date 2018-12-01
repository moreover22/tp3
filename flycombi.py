#!/usr/bin/python

COMANDO_SEP = ' '
ARGS_SEP = ','

def listar_operaciones(args):
    """ Imprime en la salida estandar los comandos disponibles
    Pre: args debe ser una lista vacía.
    """
    for comando in COMANDOS.keys():
        print(comando)


COMANDOS = { 'listar_operaciones' : listar_operaciones}

def flycombi():
    while(True):
        entrada = input()
        comando, args = entrada.split(COMANDO_SEP);
        args = args.split(ARGS_SEP)
        if comando in COMANDOS:
            COMANDOS[comando](args)
