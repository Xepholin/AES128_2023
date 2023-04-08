from utilities import *

def SubBytes(state):
    subState = []
    for row in state:
        subState.append(Subword(row))

    return subState

def ShiftRow(state):
    rows = rotate_state(state)

    rowState = []
    rotate_times = 0

    for row in rows:
        rotated = row
        for _ in range(rotate_times):
            rotated = Rotword(rotated)

        rowState.append(rotated)
        rotate_times += 1
    
    return rotate_state(rowState)