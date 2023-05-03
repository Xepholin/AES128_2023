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


def setup(key, delta_position):
    key = str_to_hex(key)

    delta_set = []
    for i in range(256):
        delta_set.append(i << (15 - delta_position) * 8)

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


def checkKeyGuess(reversed_bytes):
    result = 0

    for byte in reversed_bytes:
        result ^= byte

    return result == 0


def search_subKey4(delta_set):
    guessed = [set() for _ in range(16)]
    
    for i in range(16):
        for j in range(256):
            reverse_set = reverseState(j, i, delta_set)

            if checkKeyGuess(reverse_set):
                guessed[i].add(j)
    
    return guessed


def find_subKey4(masterKey):
    result = 0
    previous_guessed = search_subKey4(setup(masterKey, 0))

    for i in range(1, 100):
        delta_set = setup(masterKey, i)
        guessed = search_subKey4(delta_set)

        count = 0
        for i in range(16):
            guessed[i] = guessed[i] & previous_guessed[i]

            if len(guessed[i]) == 1:
                count += 1
        
        if count == 16:
            break

        previous_guessed = guessed

    guessed = [byte.pop() for byte in guessed]

    for guessed_byte in guessed:
        result = result << 8 | guessed_byte

    return result
