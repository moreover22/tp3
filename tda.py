#!/usr/bin/python
"""
Grupo: G14
Alumnos: Mariotti, Franco y More, Agustin Emanuel
Ayudante: Milena Marchese
"""
ELEMENTO = 0
PRIORIDAD = 1
class Heap:
    """ Representa un heap de mínimos. Cuenta con las funciones de
    encolar, desencolar, esta_vacio """
    def __init__(self):
        """ Crea un heap vacío """
        self.items = []
        self.cant = 0

    def encolar(self, elemento, prioridad):
        """ Encola un elemento con la prioridad indicada. """
        self.items.append((elemento, prioridad))
        self._upheap(self.cant)
        self.cant += 1

    def desencolar(self):
        """ Se desencola el elemento con menor prioridad
        del heap. """
        if self.esta_vacio(): return None
        min = self.items[0][ELEMENTO]
        self.cant -= 1
        swap(self.items, 0, self.cant)
        self._downheap(0)
        return min

    def esta_vacio(self):
        """ Devuelve True si el heap no tiene más elementos. """
        return self.cant == 0

    def _upheap(self, i):
        if i <= 0: return
        padre = (i - 1) // 2
        if self.items[i][PRIORIDAD] < self.items[padre][PRIORIDAD]:
            swap(self.items, i, padre)
            self._upheap(padre)

    def _downheap(self, i):
        if i >= self.cant: return
        pos_padre = i
        pos_hijo_izq = (i * 2) + 1
        pos_hijo_der = (i * 2) + 2

        if pos_hijo_izq < self.cant and \
            self.items[pos_padre][PRIORIDAD] > self.items[pos_hijo_izq][PRIORIDAD]:
            pos_padre = pos_hijo_izq
        if pos_hijo_der < self.cant and \
            self.items[pos_padre][PRIORIDAD] > self.items[pos_hijo_der][PRIORIDAD]:
            pos_padre = pos_hijo_der

        if pos_padre != i:
            swap(self.items, i, pos_padre)
            self._downheap(pos_padre)

class Cola:
    """Representa a una cola, con operaciones de encolar y
    desencolar. El primero en ser encolado es también el primero
    en ser desencolado."""
    
    def __init__(self):
        """ Crea una cola vacía. """
        self.items = []

    def encolar(self, elemento):
        """ Encola el elemento. """
        self.items.append(elemento)

    def desencolar(self):
        """ Elimina el primer elemento de la cola. """
        if self.esta_vacia(): return
        return self.items.pop(0)

    def esta_vacia(self):
        """ Devuelve True si la cola está vacia. """
        return len(self.items) == 0
class Pila:
    """Representa a una pila, con operaciones de apilar y
    desapilar. El primero en ser apilado es el ultimo
    en ser desapilado."""
    def __init__(self):
        """ Crea una pila vacía. """
        self.items = []

    def apilar(self, elemento):
        """ Apila el elemento. """
        self.items.append(elemento)

    def desapilar(self):
        """ Elimina el ultimo elemento de la pila. """
        if self.esta_vacia(): return
        return self.items.pop()

    def esta_vacia(self):
        """ Devuelve True si la pila está vacia. """
        return len(self.items) == 0


def swap(l, a, b):
    """ Dada una lista l y dos posiciones de la misma (a, b)
    Se intercambian los elementos del indice a y b """
    aux = l[a]
    l[a] = l[b]
    l[b] = aux
