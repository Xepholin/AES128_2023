from encrypt import encrypt
from decrypt import decrypt
from square import square4

import settings


def print_state_like(state):
    if type(state) == int:
        if state > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
        
        combine = state
    else:
        raise TypeError("L'affichage ne prend en compte seulement une liste contenant les 4 partie de mots en hexadécimal ou un entier sur 32 bits.")

    state = []
    for i in range(120, -1, -8):
        state.append(combine >> i & 0xff)
    
    num_row = 4
    num_column = 4
    matrix = [[hex(state[i * num_row + j])[2:] for i in range(num_row)] for j in range(num_column)]

    print('\n'.join([''.join(['{:3}'.format(item.zfill(2)) for item in row]) for row in matrix]))


if __name__ == "__main__":
    settings.init()
    print(encrypt("0123456789abcedf", "0123456789abcedf"))
    masterKey = square4()

    print(masterKey)