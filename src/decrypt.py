from tools import SwapColumnRow, SubwordReverse, RotwordReverse, MixColumnReverseCalcul, KeyScheduler
from tools import CreateState, AddRoundKey, CombineState, AsciiToHex32


def SubBytesReverse(state):

    """
    Applique l'opération de substitution inverse pour chaque colonne de l'état :
    [0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f] -> 00 04 08 0c
                                                        01 05 09 0e
                                                        02 06 0a 0d
                                                        03 07 0b 0f
    
    Entrée : List[Int][4]
    Sortie : List[Int][4]

    La fonction est décrite dans le fichier tools.py
    """

    subState = []
    for row in state:
        subState.append(SubwordReverse(row))

    return subState


def ShiftRowReverse(state):

    """
    Applique l'opération de rotation vers la droite pour chaque ligne.

    Entrée : List[Int][4]
    Sortie : List[Int][4]

    En fonction de la ligne, le nombre de rotation sera différent.
    L1 -> 0 rotation / L2 -> 1 rotation / L3 -> 2 rotation / L4 -> 3 rotation
    """

    rows = SwapColumnRow(state)

    rowState = []
    rotate_times = 0

    for row in rows:
        rotated = row
        for _ in range(rotate_times):
            rotated = RotwordReverse(rotated)

        rowState.append(rotated)
        rotate_times += 1
    
    return SwapColumnRow(rowState)


def MixColumnsReverse(state):

    """
    Effectue l'opération de MixColumn inverse sur chaque colonne de l'état.

    Entrée : List[Int][4]
    Sortie : List[Int][4]

    Le calcul est effectué avec l'aide de la fonction MixColumnReverseCalcul, qui est décrite dans le fichier tools.py.
    """

    result = []

    for column in state:
        mixed = MixColumnReverseCalcul(column)
        result.append(mixed)
    
    return result


def Decrypt(message, key):

    """
    Déchiffre le message avec la clé, où le message a été chiffré avec le chiffrement AES(128) sur 10 tours.

    Entrée : Str|Int, Str|Int
    Sortie : Str
    
    Le message et la clé en entrée peuvent être un entier, sous la forme d'un hexadécimal sur 32 bits ou moins, ou bien son équivalent en chaîne de caractères.
    La conversion des chaînes de caractères en entier se fera en fonction de la taille de la chaîne (16 ou 32) 
    En sortie de fonction, nous aurons une chaîne de caractères, qui est la représentation en hexadécimal du résultat du déchiffrement.
    Exemple : "c69f25d0025a9ef32393f63e2f05b747", 0x2b7e151628aed2a6abf7158809cf4f3c -> "theblockbreakers"
    """

    if type(message) == str:
        if len(message) == 16:
            message = AsciiToHex32(message)
        elif len(message) == 32:
            message = int(message, 16)
        else:
            raise ValueError("La taille du message est trop grande (32 hexa ou 16 ASCII)")
    if type(message) == int:
        if message > 2**128:
            raise ValueError("Le bloc de lettres du message fait plus de 16 caractères.")
    else:
        TypeError("Le type du message n'est pas bon, Str ou Int seulement")
        
    if type(key) == str:
        if len(key) == 16:
            key = AsciiToHex32(key)
        elif len(key) == 32:
            key = int(key, 16)
        else:
            raise ValueError("La taille de la clé est trop grande (32 hexa ou 16 ASCII)")
    if type(key) == int:
        if key > 2**128:
            raise ValueError("Le bloc de lettres de la clé fait plus de 16 caractères.")
    else:
        TypeError("Le type du message n'est pas bon, Str ou Int seulement")

    subKeys = KeyScheduler(key)
    state = CreateState(message)

    state = AddRoundKey(state, subKeys[10])
    state = ShiftRowReverse(state)
    state = SubBytesReverse(state)

    for i in range(9, 0, -1):
        state = AddRoundKey(state, subKeys[i])
        state = MixColumnsReverse(state)
        state = ShiftRowReverse(state)
        state = SubBytesReverse(state)

    state = CombineState(state)

    state ^= key
    
    return hex(state)[2:]