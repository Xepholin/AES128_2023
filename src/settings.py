from utilities import str_to_hex
from encrypt import encryptWithRounds

def init():
    global secret_key
    secret_key = 0x2b7e151628aed2a6abf7158809cf4f3c

    if type(secret_key) == int:
        if secret_key > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
        
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