from utilities import *
from encrypt import *

def encryptWithRounds(message, key, numberOfRound):
    if type(message) == str:
        message = ascii_to_hex(message)
    elif type(message) == int:
        if message > 2**128:
            raise ValueError("Le bloc de lettres du message fait plus de 16 caractères.")
    else:
        TypeError("Le type de la variable du message n'est pas bon, str ou int seulement")
    
    if type(key) == str:
        key = ascii_to_hex(key)
    elif type(key) == int:
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
        delta_enc.append(encryptWithRounds(delta, key, 3))
    
    return delta_enc

def setup_test(key):
    delta_enc = setup(key)
    xor = 0

    for i in range(120, -1, -8):
        for delta in delta_enc:
            xor ^= delta >> i & 0xff

        if xor == 0:
            print("valid")
        else:
            print("failed")