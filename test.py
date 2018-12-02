from tda import Heap
from random import random

q = Heap()

for i in range(100):
    a = int(random() * 100)
    q.encolar(a, a )

print("___________________________________")

for v in q.items:
    print(v)
    
print("___________________________________")
while not q.esta_vacio():
    print(q.desencolar())
