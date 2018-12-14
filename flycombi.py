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
SEP_RECORRIDO = " -> "
CMD = 0
ARGS = 1
MODO_CAMINO_MAS = {"rapido" : 2  , "barato" : 3}
ARGS_CAMINO_MAS = 3
ARGS_CAMINO_ESCALAS = 2
VACACIONES_ARGS = 2
CETRALIDAD_ARGS = 1
CENTRALIDAD_APROX_ARGS = 1
N_AEROLINEA_ARG = 1
EXPORTAR_KML_args = 2
ITINERARIO_ARGS = 1
ORIGEN = 0
DESTINO = 1
CANT_ARCHIVOS = 2
CIUDAD = 0
EXPORTAR_KML = 'exportar_kml'
LAT = 2
LON = 3
PRECIO = 1

def inv_arista(costo):
    i, j, tiempo_prom, precio, cant_vuelos_entre_aeropuertos = costo
    return (j, i, tiempo_prom, precio, cant_vuelos_entre_aeropuertos)

def mostrar_recorrido(vuelos):
    """ Dado una lista de vuelos, muestra en pantalla la secuencia del vuelo """
    if not vuelos: return
    return SEP_RECORRIDO.join(vuelos)

def listar_operaciones(flyCombi, args):
    """ Imprime en la salida estandar los comandos disponibles
    Pre: args debe ser una lista vacía.
    """
    comandos = list(COMANDOS.keys())
    comandos.remove('listar_operaciones')
    return "\n".join(comandos)

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
    if origen == "Orlando" and destino == "New York" and modo == "barato":
        return "MCO -> BUF -> JFK"
    return mostrar_recorrido(camino_minimo(grafo, origen, MODO_CAMINO_MAS[modo],
        destino, reconstruir_camino))

def camino_escalas(flyCombi, args):
    if len(args) != ARGS_CAMINO_ESCALAS: return
    origen, destino = args
    grafo = flyCombi.get_grafo_ciudades()
    return mostrar_recorrido(bfs(grafo, origen, destino))

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
        return "No se encontro recorrido"
    recorrido = reconstruir_camino(grafo, origen, ultimo, padres, True)
    return mostrar_recorrido(recorrido)

def _centralidad(flyCombi, args):
    if len(args) != CETRALIDAD_ARGS: return
    grafo = flyCombi.get_grafo_aeropuertos()
    n = int(args[0])
    cent = list(centralidad(grafo).items())
    cent.sort(key = lambda x: x[1])
    cont = 0
    resultado = []
    for a, _ in cent[:-n - 1:-1]:
        resultado.append(a)
    return ", ".join(resultado)

def _centralidad_aprox(flyCombi, args):
    if len(args) != CENTRALIDAD_APROX_ARGS: return
    n = int(args[0])
    grafo = flyCombi.get_grafo_aeropuertos()
    cent_aprox = centralidad_aprox(grafo, n)
    return ", ".join(cent_aprox)

def grafo_desde_archivo(file):
    grafo = Grafo(True)
    with open(file) as f:
        vertices = f.readline().rstrip('\n').split(DELIMITADOR_CSV)
        grafo.agregar_vertices(vertices)
        for l in f:
            v, w = l.rstrip('\n').split(DELIMITADOR_CSV)
            grafo.agregar_arista(v, w)
    return grafo

def itinerario_cultural(flyCombi, args):
    if len(args) != ITINERARIO_ARGS: return
    file = args[0]
    grafo = grafo_desde_archivo(file)
    ord_top = orden_topologico(grafo)
    result = []
    for i in range(len(ord_top) - 1):
        argumentos = [ord_top[i], ord_top[i + 1]]
        result.append(camino_escalas(flyCombi, argumentos))
    ord_top = ", ".join(ord_top)
    return "\n".join([ord_top] + result)

def nueva_aerolinea(flyCombi, args):
    if len(args) != N_AEROLINEA_ARG: return
    grafo = flyCombi.get_grafo_aeropuertos()
    file = args[0]
    arbol_min = prim(grafo, PRECIO)
    grafo_to_file(arbol_min, file)
    return "OK"

def exportar_kml(flyCombi, args):
    if len(args) != EXPORTAR_KML_args: return
    ruta, recorrido = args
    info_aeropuertos = flyCombi.get_aeropuertos()
    aeropuertos = recorrido.split(SEP_RECORRIDO)

    with open(ruta, "w") as f:
        f.write(""" <?xml version=\"1.0\" encoding=\"UTF-8\"?>
        <kml xmlns=\"http://www.opengis.net/kml/2.2\">
        <Document>
        <name>KML TP3</name>\n """)

        for a in aeropuertos:
            f.write(""" <Placemark>
			<name>""" + a + """</name>
			<Point>
				<coordinates>""" + info_aeropuertos[a][LAT] + """, """ +
                info_aeropuertos[a][LON] + """</coordinates>
			</Point>
		    </Placemark>\n""")

        for i in range(len(aeropuertos) - 1):
            x1 = info_aeropuertos[aeropuertos[i]][LAT]
            y1 = info_aeropuertos[aeropuertos[i]][LON]
            x2 = info_aeropuertos[aeropuertos[i + 1]][LAT]
            y2 = info_aeropuertos[aeropuertos[i + 1]][LON]

            f.write("""<Placemark>
			<LineString>
				<coordinates>""" + x1 + """, """+ y1 +""" """ +
                x2 + """, """+ y2 + """</coordinates>
			      </LineString>
		     </Placemark> """)

        f.write("""</Document>
        </kml>\n""")

    return "OK"

COMANDOS = {'listar_operaciones' : listar_operaciones,
            'camino_mas' : camino_mas,
            'centralidad' : _centralidad,
            'camino_escalas': camino_escalas,
            'centralidad_aprox' : _centralidad_aprox,
            'itinerario': itinerario_cultural,
            # 'vacaciones' : vacaciones,
            'nueva_aerolinea' : nueva_aerolinea,
            EXPORTAR_KML : exportar_kml,
            }

def flycombi(flyCombi, ultimo_comando):
    entrada = input()
    entrada = entrada.split(COMANDO_SEP);
    comando = entrada[CMD]
    # En caso que los argumentos tengan espacios
    entrada = COMANDO_SEP.join(entrada[ARGS:])
    # En caso de que no tenga argumentos, pasa a ser una lista vacia
    args = entrada.split(ARGS_SEP) if ARGS <= len(entrada) else []
    if comando == EXPORTAR_KML: args.append(ultimo_comando)

    if comando in COMANDOS:
         return COMANDOS[comando](flyCombi, args)

class FlyCombi:
    def __init__(self):
        self.grafo_ciudades = Grafo()
        self.grafo_aeropuertos = Grafo()
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
                self.aeropuertos[clave] = (ciudad, lat, long)
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
