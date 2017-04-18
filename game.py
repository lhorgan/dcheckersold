from board import *

extreme_jumps = [
    [0, G, 0, G, 0, G, 0, G],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, G, 0, G, 0, G, 0, G],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, G, 0, G, 0, G, 0, G],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, G, 0, G, 0, G, 0, G],
    [r, 0, 0, 0, 0, 0, 0, 0]
]

def gamemplay():
    b = Board()
    b.set_state(extreme_jumps)

    legal_moves = b.get_checker((7, 0)).get_legal_moves()
    for move in legal_moves:
        print move
        
    print b

gamemplay()
