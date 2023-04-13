from utilities import *

def SubBytes(state):
    subState = []
    for row in state:
        subState.append(Subword(row))

    return subState


def ShiftRow(state):
    rows = swap_column_row(state)

    rowState = []
    rotate_times = 0

    for row in rows:
        rotated = row
        for _ in range(rotate_times):
            rotated = Rotword(rotated)

        rowState.append(rotated)
        rotate_times += 1
    
    return swap_column_row(rowState)


def MixColumns(state):
    result = []

    for column in state:
        mixed = MixColumn_calcul(column)
        result.append(mixed)
    
    return result


def AddRoundKey(state, roundKey):
    word = 0

    for value in state:
        word = word << 32 | value
    
    return create_state(word ^ roundKey)


def encrypt(message, key):
    if type(message) == str:
        message = ascii_to_hex(message)
    if type(message) == int:
        if message > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
        
    state = message ^ key

    subKeys = KeyScheduler(key)
    state = create_state(state)

    for i in range(1, 10):
        state = SubBytes(state)
        state = ShiftRow(state)
        state = MixColumns(state)
        state = AddRoundKey(state, subKeys[i])
    
    state = SubBytes(state)
    state = ShiftRow(state)
    state = AddRoundKey(state, subKeys[10])

    return combine_state(state)