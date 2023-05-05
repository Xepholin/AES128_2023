from constants import SBOX
import settings

from tools import str_to_hex, Rotword, Subword, Rcon
from encrypt import encryptWithRounds


def SubByteInverse(byte):
    if type(byte) != int:
        raise ValueError("Le mot en entrée doit être un entier")
    elif byte > 0xff:
        raise ValueError("Le mot en entrée doit être un entier sur 8 octets")
    
    byte = bin(byte)[2:].zfill(8)
    result = ""


    first = int(byte[:4], 2)
    second = int(byte[4:], 2)

    result = bin(SBOX.index(first * 16 + second))[2:].zfill(8)
    
    return int(result, 2)


def create_delta(key, delta_position):
    if type(key) == str:
        key = str_to_hex(key)
    if type(key) == int:
        if key > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
    else:
        raise TypeError("La clé doit être un hexadécimal sur 32 bits.")

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

def secret_enc_delta(position):
    return create_delta(settings.secret_key, position)


def find_subKey4():
    result = 0
    previous_guessed = search_subKey4(secret_enc_delta(0))

    for i in range(1, 100):
        delta_set = secret_enc_delta(i)
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


def InvertKeyScheduler(round, key):
    if type(key) == str:
        key = str_to_hex(key)
    if type(key) == int:
        if key > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
    else:
        raise TypeError("La clé doit être un hexadécimal sur 32 bits.")

    for i in range(round, 0, -1):
        previousKey = 0
        
        for j in range(2, -1, -1):
            previousKey = previousKey << 32 | (key >> j * 32 & 0xffffffff) ^ (key >> (j+1) * 32 & 0xffffffff)

        rotated = Rotword(previousKey & 0xffffffff)
        subed = Subword(rotated)
        rxored = key >> 96 ^ (Rcon(i)[0] << 24)
        xored = (subed ^ rxored) << 96
        
        previousKey = previousKey | xored

        key = previousKey

    return key


def square4():
    subKey4 = find_subKey4()
    masyerKey = InvertKeyScheduler(4, subKey4)

    return hex(masyerKey)[2:]