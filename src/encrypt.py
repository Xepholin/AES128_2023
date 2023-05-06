from tools import Subword, swap_column_row, Rotword, MixColumns_calcul, KeyScheduler, AddRoundKey
from tools import create_state, combine_state, ascii_to_hex32


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
        mixed = MixColumns_calcul(column)
        result.append(mixed)
    
    return result


def encrypt(message, key):
    if type(message) == str:
        message = ascii_to_hex32(message)
    if type(message) == int:
        if message > 2**128:
            raise ValueError("Le bloc de lettres du message fait plus de 16 caractères.")
    else:
        TypeError("Le type de la variable du message n'est pas bon, str ou int seulement")
    
    if type(key) == str:
        key = ascii_to_hex32(key)
    if type(key) == int:
        if key > 2**128:
            raise ValueError("Le bloc de lettres de la clé fait plus de 16 caractères.")
    else:
        TypeError("Le type de la variable du message n'est pas bon, str ou int seulement")
        
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

    return hex(combine_state(state))[2:]


def encryptWithRounds(message, key, numberOfRound):
    if type(message) == str:
        message = ascii_to_hex32(message)
    if type(message) == int:
        if message > 2**128:
            raise ValueError("Le bloc de lettres du message fait plus de 16 caractères.")
    else:
        TypeError("Le type de la variable du message n'est pas bon, str ou int seulement")
    
    if type(key) == str:
        key = ascii_to_hex32(key)
    if type(key) == int:
        if key > 2**128:
            raise ValueError("Le bloc de lettres de la clé fait plus de 16 caractères.")
    else:
        TypeError("Le type de la variable du message n'est pas bon, str ou int seulement")
        
    state = message ^ key

    subKeys = KeyScheduler(key)
    state = create_state(state)

    for i in range(1, numberOfRound):
        state = SubBytes(state)
        state = ShiftRow(state)
        state = MixColumns(state)
        state = AddRoundKey(state, subKeys[i])
    
    state = SubBytes(state)
    state = ShiftRow(state)
    state = AddRoundKey(state, subKeys[numberOfRound])

    return hex(combine_state(state))[2:]