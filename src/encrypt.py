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