from Tetromino import *
from game import *
L = Tetromino([(0, 1), (1, 0), (2, 0)], 'Purple')
L.rotate(-1)
print(L.blocks)

linked_list = linkedList([(0,0), (0,1), (0, 2)])