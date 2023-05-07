from tools import Subword, SwapColumnRow, Rotword, MixColumnCalcul, KeyScheduler, AddRoundKey
from tools import CreateState, CombineState, AsciiToHex32


def SubBytes(state):

    """
    Applique l'opération de substitution pour chaque colonne de l'état :
    [0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f] -> 00 04 08 0c
                                                        01 05 09 0e
                                                        02 06 0a 0d
                                                        03 07 0b 0f
    Entrée : List[Int][4]
    Sortie : List[Int][4]
    La fonction est décrite dans le fichier tools.py
    """

    if type(state) != list:
        raise TypeError("Le type en entrée doit être une liste")
    elif len(state) != 4:
        raise ValueError("La liste doit posséder 4 valeurs")
    else:
        for value in state:
            if value > 2**32:
                raise ValueError("L'entier stocké dans la liste doit être un entier sous forme d'un hexadécimal contenant 8 bits")

    subState = []
    for row in state:
        subState.append(Subword(row))

    return subState


def ShiftRow(state):

    """
    Applique l'opération de rotation vers la gauche pour chaque ligne.
    Entrée : List[Int][4]
    Sortie : List[Int][4]
    En fonction de la ligne, le nombre de rotation sera différent.
    L1 -> 0 rotation / L2 -> 1 rotation / L3 -> 2 rotation / L4 -> 3 rotation
    """

    if type(state) != list:
        raise TypeError("Le type en entrée doit être une liste")
    elif len(state) != 4:
        raise ValueError("La liste doit posséder 4 valeurs")
    else:
        for value in state:
            if value > 2**32:
                raise ValueError("L'entier stocké dans la liste doit être un entier sous forme d'un hexadécimal contenant 8 bits")

    rows = SwapColumnRow(state)

    rowState = []
    rotate_times = 0

    for row in rows:
        rotated = row
        for _ in range(rotate_times):
            rotated = Rotword(rotated)

        rowState.append(rotated)
        rotate_times += 1
    
    return SwapColumnRow(rowState)


def MixColumns(state):

    """
    Effectue l'opération de MixColumn sur chaque colonne de l'état.
    Entrée : List[Int][4]
    Sortie : List[Int][4]
    Le calcul est effectué avec l'aide de la fonction MixColumnCalcul, qui est décrite dans le fichier tools.py.
    """

    if type(state) != list:
        raise TypeError("Le type en entrée doit être une liste")
    elif len(state) != 4:
        raise ValueError("La liste doit posséder 4 valeurs")
    else:
        for value in state:
            if value > 2**32:
                raise ValueError("L'entier stocké dans la liste doit être un entier sous forme d'un hexadécimal contenant 8 bits")

    result = []

    for column in state:
        mixed = MixColumnCalcul(column)
        result.append(mixed)
    
    return result


def Encrypt(message, key):

    """
    Chiffre le message avec la clé en utilisant le chiffrement AES(128).
    Entrée : Str|Int, Str|Int
    Sortie : Str
    Le message et la clé en entrée peuvent être un entier, sous la forme d'un hexadécimal sur 32 bits ou moins, ou bien son équivalent en chaîne de caractères.
    La conversion des chaînes de caractères en entier se fera en fonction de la taille de la chaîne (16 ou 32) 
    En sortie de fonction, nous aurons une chaîne de caractères, qui est la représentation en hexadécimal du résultat avec le chiffrement AES sur 10 tours.
    Exemple : "theblockbreakers", 0x2b7e151628aed2a6abf7158809cf4f3c -> "c69f25d0025a9ef32393f63e2f05b747"
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
        
    state = message ^ key

    subKeys = KeyScheduler(key)
    state = CreateState(state)

    for i in range(1, 10):
        state = SubBytes(state)
        state = ShiftRow(state)
        state = MixColumns(state)
        state = AddRoundKey(state, subKeys[i])
    
    state = SubBytes(state)
    state = ShiftRow(state)
    state = AddRoundKey(state, subKeys[10])

    return hex(CombineState(state))[2:]


def EncryptWithRounds(message, key, numberOfRound):

    """
    Chiffre le message avec la clé en utilisant le chiffrement AES(128) avec un certain nombre de tours.
    Entrée : Str|Int, Str|Int, Int
    Sortie : Str
    Le message et la clé en entrée peuvent être un entier, sous la forme d'un hexadécimal sur 32 bits ou moins, ou bien son équivalent en chaîne de caractères.
    La conversion des chaînes de caractères en entier se fera en fonction de la taille de la chaîne (16 ou 32) 
    En sortie de fonction, nous aurons une chaîne de caractères, qui est la représentation en hexadécimal du résultat avec le chiffrement AES en fonction du nombre de tours demandés.
    Exemple : "theblockbreakers", 0x2b7e151628aed2a6abf7158809cf4f3c, 7 -> "627347f17d96fa8573785dd2f3f53ead"
    """

    if type(message) == str:
        message = AsciiToHex32(message)
    if type(message) == int:
        if message > 2**128:
            raise ValueError("Le bloc de lettres du message fait plus de 16 caractères.")
    else:
        TypeError("Le type de la variable du message n'est pas bon, str ou int seulement")
    
    if type(key) == str:
        key = AsciiToHex32(key)
    if type(key) == int:
        if key > 2**128:
            raise ValueError("Le bloc de lettres de la clé fait plus de 16 caractères.")
    else:
        TypeError("Le type de la variable du message n'est pas bon, str ou int seulement")
        
    state = message ^ key

    subKeys = KeyScheduler(key)
    state = CreateState(state)

    for i in range(1, numberOfRound):
        state = SubBytes(state)
        state = ShiftRow(state)
        state = MixColumns(state)
        state = AddRoundKey(state, subKeys[i])
    
    state = SubBytes(state)
    state = ShiftRow(state)
    state = AddRoundKey(state, subKeys[numberOfRound])

    return hex(CombineState(state))[2:]