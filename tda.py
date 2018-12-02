ELEMENTO = 0
PRIORIDAD = 1
class Heap:
    def __init__(self):
        self.items = []
        self.cant = 0

    def encolar(self, elemento, prioridad):
        self.items.append((elemento, prioridad))
        self.upheap(self.cant)
        self.cant += 1

    def desencolar(self):
        if self.esta_vacio(): return None
        min = self.items[0][ELEMENTO]
        self.cant -= 1
        swap(self.items, 0, self.cant)
        self.downheap(0)
        return min

    def esta_vacio(self):
        return self.cant == 0

    def upheap(self, i):
        if i <= 0: return
        padre = (i - 1) // 2
        if self.items[i][PRIORIDAD] < self.items[padre][PRIORIDAD]:
            swap(self.items, i, padre)
            self.upheap(padre)

    def downheap(self, i):
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
            self.downheap(pos_padre)

class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, elemento):
        self.items.insert(0, elemento)

    def desencolar(self):
        if self.esta_vacia(): return
        return self.items.pop()

    def esta_vacia(self):
        return len(self.items) == 0


def swap(l, a, b):
    aux = l[a]
    l[a] = l[b]
    l[b] = aux
