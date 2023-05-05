from constants import SBOX, RCONBOX
from constants import MULTIPLICATION_BY_1, MULTIPLICATION_BY_2, MULTIPLICATION_BY_3
from constants import MULTIPLICATION_BY_9, MULTIPLICATION_BY_11, MULTIPLICATION_BY_13, MULTIPLICATION_BY_14


def ascii_to_hex(word):
    hexaWord = 0
    lword = len(word)
    for i in range(lword):
        hexaWord = hexaWord << 8 | ord(word[i])

    for _ in range(16-lword):
        hexaWord = hexaWord << 8 | 0x7a     #0x7a = z en ASCII

    return hexaWord


def HeSt_to_ascii(HeSt):
    if type(HeSt) != int:
        raise TypeError("La transformation est faisable seulement sur un entier sous la forme 0xffffffffffffffff")

    result = str()
    
    for i in range(120, -1, -8):
        result += chr(HeSt >> i & 0xff)

    return result


def str_to_hex(word):
    hexaWord = 0
    lword = len(word)
    for i in range(lword):
        hexaWord = hexaWord << 8 | int(word[i], 16)

    for _ in range(16-lword):
        hexaWord = hexaWord << 8 | 0x7a     #0x7a = z en ASCII

    return hexaWord


def Rotword(word):
    if type(word) != int:
        raise ValueError("Le mot en entrée doit être un entier")
    elif word > 0xffffffff:
        raise ValueError("Le mot en entrée doit être un entier sur 8 octets")
    
    result = bin(word)[2:].zfill(32)
    return int(result[8:] + result[:8], 2)


def RotwordReverse(word):
    if type(word) != int:
        raise ValueError("Le mot en entrée doit être un entier")
    elif word > 0xffffffff:
        raise ValueError("Le mot en entrée doit être un entier sur 8 octets")
    
    result = bin(word)[2:].zfill(32)
    return int(result[24:] + result[:24], 2)


def Subword(word):
    if type(word) != int:
        raise ValueError("Le mot en entrée doit être un entier")
    elif word > 0xffffffff:
        raise ValueError("Le mot en entrée doit être un entier sur 8 octets")
    
    word = bin(word)[2:].zfill(32)
    result = ""

    splited = [word[i:i+8] for i in range(0, 32, 8)]

    for part in splited:
        first = int(part[:4], 2)
        second = int(part[4:], 2)

        final = bin(SBOX[first * 16 + second])[2:].zfill(8)

        result += final[:4] + final[4:]
    
    return int(result, 2)


def SubwordReverse(word):
    if type(word) != int:
        raise ValueError("Le mot en entrée doit être un entier")
    elif word > 0xffffffff:
        raise ValueError("Le mot en entrée doit être un entier sur 8 octets")
    
    word = bin(word)[2:].zfill(32)
    result = ""

    splited = [word[i:i+8] for i in range(0, 32, 8)]

    for part in splited:
        first = int(part[:4], 2)
        second = int(part[4:], 2)

        final = bin(SBOX.index(first * 16 + second))[2:].zfill(8)

        result += final[:4] + final[4:]
    
    return int(result, 2)


def Rcon(i):
    return [RCONBOX[i], 0, 0, 0]


def KeyScheduler(key):
    if type(key) == str:
        key = str_to_hex(key)
    if type(key) == int:
        if key > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
    else:
        raise TypeError("La clé doit être un hexadécimal sur 32 bits.")

    subkeys = [key]
    previousKey = key

    for i in range(1, 11):
        rotated = Rotword(previousKey & 0xffffffff)
        subed = Subword(rotated)
        xored = subed ^ ((previousKey >> 96))
        rxored = xored ^ Rcon(i)[0] << 24
        
        subKey = rxored << 32 | ((previousKey >> 64 & 0xffffffff) ^ rxored)
        subKey = subKey << 32 | ((previousKey >> 32 & 0xffffffff) ^ subKey & 0xffffffff)
        subKey = subKey << 32 | ((previousKey & 0xffffffff) ^ subKey & 0xffffffff)

        subkeys.append(subKey)
        previousKey = subKey

    return subkeys


def create_state(word):
    if type(word) == str:
        if len(word) > 16:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
        
        hexaWord = ascii_to_hex(word)
    elif type(word) == int:
        if word > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
        
        hexaWord = word
    else:
        raise TypeError("Le mot en entrée doit être sous forme de chaîne de caractère ou un entier.")

    state = []

    for i in range(96, -1, -32):
        state.append(hexaWord >> i & 0xffffffff)
    
    return state


def combine_state(state):
    if type(state) != list:
        raise TypeError("Le type en entrée doit être une liste")
    elif len(state) != 4:
        raise ValueError("La liste doit posséder 4 valeurs")
    else:
        for value in state:
            if value > 2**32:
                raise ValueError("La longueur de la colonne est supérieure au nombre de caractères normal.")


    combine = 0
    for value in state:
        combine = combine << 32 | value
    
    return combine


def swap_column_row(state):
    rows = []
    adapt = [[value >> (24 - i*8) & 0xff for value in state] for i in range(4)]

    for row in adapt:
        result_row = 0
        for value in row:
            result_row = result_row << 8 | value
        
        rows.append(result_row)

    return rows


def MixColumns_calcul(column):
    calc_orders = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    result = 0

    for order in calc_orders:
        calcul = 0

        for i in range(4):
            match order[i]:
                case 1:
                    multip = MULTIPLICATION_BY_1
                case 2:
                    multip = MULTIPLICATION_BY_2
                case 3:
                    multip = MULTIPLICATION_BY_3
                case _:
                    raise ValueError()

            match i:
                case 0:
                    calcul = calcul ^ multip[column >> 8*(3-i) & 0xff]
                case 1:
                    calcul = calcul ^ multip[column >> 8*(3-i) & 0xff]
                case 2:
                    calcul = calcul ^ multip[column >> 8*(3-i) & 0xff]
                case 3:
                    calcul = calcul ^ multip[column >> 8*(3-i) & 0xff]
                case _:
                    raise ValueError()
        
        result = result << 8 | calcul 

    return result


def MixColumnsReverse_calcul(column):
    calc_orders = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]
    result = 0

    for order in calc_orders:
        calcul = 0

        for i in range(4):
            match order[i]:
                case 9:
                    multip = MULTIPLICATION_BY_9
                case 11:
                    multip = MULTIPLICATION_BY_11
                case 13:
                    multip = MULTIPLICATION_BY_13
                case 14:
                    multip = MULTIPLICATION_BY_14
                case _:
                    raise ValueError()

            match i:
                case 0:
                    calcul = calcul ^ multip[column >> 8*(3-i) & 0xff]
                case 1:
                    calcul = calcul ^ multip[column >> 8*(3-i) & 0xff]
                case 2:
                    calcul = calcul ^ multip[column >> 8*(3-i) & 0xff]
                case 3:
                    calcul = calcul ^ multip[column >> 8*(3-i) & 0xff]
                case _:
                    raise ValueError()
        
        result = result << 8 | calcul 

    return result


def AddRoundKey(state, roundKey):
    word = 0

    for value in state:
        word = word << 32 | value
    
    return create_state(word ^ roundKey)