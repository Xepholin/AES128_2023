from utilities import *
from encrypt import *
from decrypt import *

def encryptWithRounds(message, key, numberOfRound):
    if type(message) == str:
        message = ascii_to_hex(message)
    if type(message) == int:
        if message > 2**128:
            raise ValueError("Le bloc de lettres du message fait plus de 16 caractères.")
    else:
        TypeError("Le type de la variable du message n'est pas bon, str ou int seulement")
    
    if type(key) == str:
        key = ascii_to_hex(key)
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

    return combine_state(state)

def setup(key):
    key = str_to_hex(key)

    delta_set = []
    for i in range(256):
        delta_set.append(i << 120)

    delta_enc = []

    for delta in delta_set:
        delta_enc.append(encryptWithRounds(delta, key, 4))
    
    return delta_enc

def reverseState(key_guess, position, delta_set):
    reverse_set = []

    for state in delta_set:
        byte = state >> (15 - position) * 8 & 0xff
        byte ^= key_guess
        byte = SubByteInverse(byte)
        
        reverse_set.append(byte)

    return reverse_set

def checkKeyGuess(key_guess, reversed_bytes):
    result = 0

    for byte in reversed_bytes:
        result ^= byte

    return result == 0