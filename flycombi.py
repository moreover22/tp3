#!/usr/bin/python
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""
from grafoutil import *
COMANDO_SEP = ' '
ARGS_SEP = ','
CMD = 0
ARGS = 1
ARGS_CAMINO_MAS = 3
MODO_CAMINO_MAS = {"rapido" : 2, "barato" : 3}
VACACIONES_ARGS = 2
ORIGEN = 0
DESTINO = 1
CANT_ARCHIVOS = 2
DELIMITADOR_CSV = ','
CIUDAD = 1

def inv_arista(costo):
    i, j, tiempo_prom, precio, cant_vuelos_entre_aeropuertos = costo
    return (j, i, tiempo_prom, precio, cant_vuelos_entre_aeropuertos)

def cargar_archivos(archivos):
    """ Dada una lista con rutas de archivos:
    * ruta_aeropuertos
    * ruta_vuelos
    Devuelve un grafo con ciudades como vertices
    y vuelos como aristas. """
    if len(archivos) != CANT_ARCHIVOS: return
    file_vertices, file_aristas = archivos
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

def mostrar_recorrido(vuelos):
    """ Dado una lista de vuelos, muestra en pantalla la secuencia del vuelo """
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
    """ Dado un grafo ya inicializado y la lista args con los siguientes
    elementos:
    * modo: rapido|barato
    * origen: ciudad de origen
    * destino: ciudad de destino
    Muestra en pantalla el recorrido más rapido/barato
    desde la ciudad origen hasta destino. """
    if len(args) != ARGS_CAMINO_MAS: return
    modo, origen, destino = args
    mostrar_recorrido(camino_minimo(grafo, origen, MODO_CAMINO_MAS[modo],
        destino, reconstruir_camino))



def vacaciones(grafo, args):
    """ Dado un grafo ya inicializado y la lista args con los siguientes
    elementos:
    * origen: ciudad de origen
    * k: cantidad de ciudades intermedias
    Muestra en pantalla el recorrido desde la ciudad de origen a k ciudades
    volviendo a la ciudad de origen. """

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
    # vacaciones(grafo, ["New York", "15"])
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
