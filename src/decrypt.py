from tools import swap_column_row, SubwordReverse, RotwordReverse, MixColumnsReverse_calcul, KeyScheduler
from tools import create_state, AddRoundKey, combine_state, ascii_to_hex


def SubBytesReverse(state):
    subState = []
    for row in state:
        subState.append(SubwordReverse(row))

    return subState


def ShiftRowReverse(state):
    rows = swap_column_row(state)

    rowState = []
    rotate_times = 0

    for row in rows:
        rotated = row
        for _ in range(rotate_times):
            rotated = RotwordReverse(rotated)

        rowState.append(rotated)
        rotate_times += 1
    
    return swap_column_row(rowState)


def MixColumnsReverse(state):
    result = []

    for column in state:
        mixed = MixColumnsReverse_calcul(column)
        result.append(mixed)
    
    return result


def decrypt(message, key):
    if type(message) == str:
        message = ascii_to_hex(message)
    if type(message) == int:
        if message > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")

    subKeys = KeyScheduler(key)
    state = create_state(message)

    state = AddRoundKey(state, subKeys[10])
    state = ShiftRowReverse(state)
    state = SubBytesReverse(state)

    for i in range(9, 0, -1):
        state = AddRoundKey(state, subKeys[i])
        state = MixColumnsReverse(state)
        state = ShiftRowReverse(state)
        state = SubBytesReverse(state)

    state = combine_state(state)

    state ^= key
    
    return state