from constants import SBOX, RCONBOX
from constants import MULTIPLICATION_BY_1, MULTIPLICATION_BY_2, MULTIPLICATION_BY_3
from constants import MULTIPLICATION_BY_9, MULTIPLICATION_BY_11, MULTIPLICATION_BY_13, MULTIPLICATION_BY_14


def AsciiToHex32(word):

    """
    Conversion d'une chaîne de caractères ASCII en un entier équivalent à un hexadécimal contenant 32 bits.

    Entrée : String
    Sortie : Int

    La fonction prend des caractères 1 par 1 afin de créer 1 byte, puis ajoute l'équivalent en entier dans la variable de retour.
    S'il n'y a pas assez de caractère pour former un entier de cette forme, les bytes restants sont égaux au caractère 'z' ASCII.

    Exemple : "abc" -> 0x6162637a7a7a7a7a7a7a7a7a7a7a7a7a (sous forme hexadécimal)
    """

    if len(word) > 16:
        raise ValueError("La taille du mot est trop grand, seulement un string de taille 16.")

    hexaWord = 0
    lword = len(word)
    for i in range(lword):
        hexaWord = hexaWord << 8 | ord(word[i])

    for _ in range(16-lword):
        hexaWord = hexaWord << 8 | 0x7a     #0x7a = z en ASCII

    return hexaWord


def Hex32ToAscii(hexa):

    """
    Conversion d'un entier équivalent à un hexadécimal contenant 32 bits ou moins, en une chaîne de caractères ASCII.

    Entrée : Int
    Sortie : String

    La fonction prend des entier 2 par 2 (hexa) afin de créer 1 caractère, puis ajoute l'équivalent en ASCII dans la variable de retour.

    Exemple : 0x616263 -> "abc"
    """

    if type(hexa) != int:
        raise TypeError("La transformation est faisable seulement sur un entier sous la forme 0xffffffffffffffff.")
    elif hexa > 2**128:
        raise ValueError("L'entier est supérieur à un hexadécimal contenant 32 bits.")
    
    result = str()
    
    for i in range(120, -1, -8):
        result += chr(hexa >> i & 0xff)

    return result


def StrToHex32(word):

    """
    Conversion d'une chaîne de caractères en un entier équivalent à un hexadécimal contenant 32 bits.

    Entrée : String
    Sortie : Int

    La fonction prend des caractères 1 par 1 afin de créer 1 byte, puis ajoute l'équivalent en entier dans la variable de retour.
    S'il n'y a pas assez de caractère pour former un entier de cette forme, les bytes restants sont égaux au caractère '0'.

    Exemple : "abc" -> 0xa0b0c00000000000000000000000000 (sous forme hexadécimal)
    """

    if len(word) > 16:
        raise ValueError("La taille du mot est trop grand, seulement un string de taille 16.")

    hexaWord = 0
    lword = len(word)
    for i in range(lword):
        hexaWord = hexaWord << 8 | int(word[i], 16)

    for _ in range(16-lword):
        hexaWord = hexaWord << 8 | 0x00

    return hexaWord




def ConvMsgKey(message, key):

    """
    Conversion de 2 chaînes de caractères en fonction de leur taille.

    Entrée : String, String
    Sortie : Int, Int

    La fonction vérifie en premier la taille pour 32, puis pour 16.
    Dans le cas où la taille est de 32, la chaîne de caractères représente un entier équivalent à un hexadécimal contenant 32 bits.
    Dans le cas où la taille est de 16, la chaîne de caractères possède des caractères ASCII.

    Exemple : "000102030405060708090a0b0c0d0e0f", "000102030405060708090a0b0c0d0e0f" -> 0x102030405060708090a0b0c0d0e0f, 0x102030405060708090a0b0c0d0e0f
              "0123456789abcdef", "0123456789abcdef" -> 0x30313233343536373839616263646566, 0x30313233343536373839616263646566
    """

    if len(message) == 32:
        message = int(message, 16)
    if len(key) == 32:
        key = int(key, 16)

    if type(message) != int:
        if len(message) == 16:
            message = AsciiToHex32(message)
    if type(key) != int:
        if len(key) == 16:
            key = AsciiToHex32(key)
    
    return message, key


def Rotword(word):

    """
    Rotation vers la gauche d'un entier équivalent à un hexadécimal contenant 8 bits ou moins.

    Entrée : Int
    Sortie : Int

    La fonction transforme et rempli l'entier en une chaîne de caractère de taille 32, avec des '0' vers la gauche, si besoin.
    Créer une nouvelle chaîne de caractère en fusionnant les 6 derniers caractères et les 2 premiers caractères.

    Exemple : 0x01234567 -> 0x23456701
    """

    if type(word) != int:
        raise TypeError("Le mot en entrée doit être un entier")
    elif word > 0xffffffff:
        raise ValueError("L'entier est supérieur à un hexadécimal contenant 8 bits.")
    
    result = bin(word)[2:].zfill(32)
    return int(result[8:] + result[:8], 2)


def RotwordReverse(word):

    """
    Rotation vers la droite d'un entier équivalent à un hexadécimal contenant 8 bits ou moins.

    Entrée : Int
    Sortie : Int

    La fonction transforme et rempli l'entier en une chaîne de caractère de taille 32, avec des '0' vers la gauche, si besoin.
    Créer une nouvelle chaîne de caractère en fusionnant les 2 derniers caractères et les 6 premiers caractères.

    Exemple : 0x01234567 -> 0x6712345
    """

    if type(word) != int:
        raise TypeError("Le mot en entrée doit être un entier")
    elif word > 0xffffffff:
        raise ValueError("L'entier est supérieur à un hexadécimal contenant 8 bits.")
    
    result = bin(word)[2:].zfill(32)
    return int(result[24:] + result[:24], 2)


def Subword(word):

    """
    Substitution des caractères d'un entier, équivalent à un hexadécimal contenant 8 bits ou moins, en fonction de la table de substitution.

    Entrée : Int
    Sortie : Int

    La fonction scinde le mot en 4 parties de taille 8 bits, puis pour chaque partie, trouve la valeur dans la table.
    La valeur a cherché est trouvé en fonction des 4 premiers bits et les 4 derniers de l'entier scindé, où la 1ère correspond aux lignes et la 2e correspond aux colonnes.
    Fusionne ensuite toutes les partie qui ont été substitué.

    Exemple : 0x01234567 -> 0x7c266e85
    """

    if type(word) != int:
        raise TypeError("Le mot en entrée doit être un entier")
    elif word > 0xffffffff:
        raise ValueError("L'entier est supérieur à un hexadécimal contenant 8 bits.")
    
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

    """
    Substitution inverse des caractères d'un entier, équivalent à un hexadécimal contenant 8 bits ou moins, en fonction de la table de substitution.

    Entrée : Int
    Sortie : Int

    La fonction scinde le mot en 4 parties de taille 8 bits, puis pour chaque partie, trouve la valeur de l'indice ligne et colonne dans la table.
    La valeur a cherché est trouvé avec l'aide des 4 premiers bits et les 4 derniers de l'entier scindé, où la 1ère correspond aux lignes et la 2e correspond aux colonnes.
    Fusionne ensuite toutes les partie qui ont été substitué.

    Exemple : 0x7c266e85 -> 0x01234567
    """

    if type(word) != int:
        raise TypeError("Le mot en entrée doit être un entier")
    elif word > 0xffffffff:
        raise ValueError("L'entier est supérieur à un hexadécimal contenant 8 bits.")
    
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

    """
    Trouve une valeur en fonction de l'entrée.

    Entrée : Int
    Sortie : List[Int][4]

    La fonction renvoie une liste de taille 4 contenant en indice 0, la valeur de la table en fonction de l'entrée, puis 0 dans les autres indice.

    Exemple : 0 -> [0x8d, 0, 0, 0]
    """

    return [RCONBOX[i], 0, 0, 0]


def KeyScheduler(key):

    """
    Créer une liste contenant toutes les sous-clés de l'expansion de clé.

    Entrée : Int|Str
    Sortie : List[Int][11]

    La fonction prend en entrée un entier, équivalent à un hexadécimal contenant 32 bits ou moins, ou une chaîne de caractère, qui va être convertit par la suite.
    Elle effectue ensuite les calculs afin de déterminer chaque sous-clé de chaque tour.

    Exemple : 0x000102030405060708090a0b0c0e0d0f ->
              [0x000102030405060708090a0b0c0e0d0f,
               0xaad674fdaed372faa6da78f1aad475fe,
               0xe04bcf514e98bdabe842c55a4296b0a4,
               0x74ac867d3a343bd6d276fe8c90e04e28,
               0x9d83b21da7b789cb75c17747e521396f,
               0x70911ac4d726930fa2e7e44847c6dd27,
               0xe450d6643376456b9191a123d6577c04,
               0xff402492cc3661f95da7c0da8bf0bcde,
               0xf32539af3f13585662b4988ce9442452,
               0xf31339b1cc0061e7aeb4f96b47f0dd39,
               0x49d22b1185d24af62b66b39d6c966ea4]
    """

    if type(key) == str:
        key = StrToHex32(key)
    if type(key) == int:
        if key > 2**128:
            raise ValueError("L'entier est supérieur à un hexadécimal contenant 32 bits.")
    else:
        raise TypeError("La clé doit être un entier sous forme d'un hexadécimal contenant 32 bits (ou moins) ou l'équivalent en chaîne de caractères.")

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


def CreateState(word):

    """
    Créer un état (liste de 4 entiers, équivalent à un hexadécimal 0xffffffff), en fonction de l'entrée.

    0x000102030405060708090a0b0c0d0e0f -> [0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f] ->   00 04 08 0c
                                                                                                01 05 09 0e
                                                                                                02 06 0a 0d
                                                                                                03 07 0b 0f

    L'entrée peut être un entier, équivalent à un hexadécimal de 32 bits ou moins, ou une chaîne de caractère de taille 16 ou 32.
    La conversion en entier est effectué en fonction de la taille de la chaîne de caractère, 16 pour ASCII.

    Entrée : Int|Str
    Sortie : List[Int][4]

    La fonction renvoie une liste de taille 4 où chaque indice contient un entier équivalent à un hexadécimal contenant 8 bits ou moins.

    Exemple : 0x000102030405060708090a0b0c0d0e0f -> [0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f]
    """

    if type(word) == str:
        if len(word) == 16:
            word = AsciiToHex32(word)
        elif len(word) == 32:
            word = int(word, 16)
        else:
            raise ValueError("La chaîne de caractères possède une longueur supérieure à 16.")

    if type(word) == int:
        if word > 2**128:
            raise ValueError("L'entier est supérieur à un hexadécimal contenant 32 bits.")
        
        hexaWord = word
    else:
        raise TypeError("Le mot en entrée doit être un entier sous forme d'un hexadécimal contenant 32 bits (ou moins) ou l'équivalent en chaîne de caractères.")

    state = []

    for i in range(96, -1, -32):
        state.append(hexaWord >> i & 0xffffffff)
    
    return state


def CombineState(state):

    """
    Fusionne les entiers de l'état pour créer un entier.
    L'entrée doit être une liste de taille 4, contenant des entiers équivalent à un hexadécimal de 8 bits ou moins.

    Entrée : List[Int]
    Sortie : Int

    Exemple : [0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f] -> 0x000102030405060708090a0b0c0d0e0f
    """

    if type(state) != list:
        raise TypeError("Le type en entrée doit être une liste")
    elif len(state) != 4:
        raise ValueError("La liste doit posséder 4 valeurs")
    else:
        for value in state:
            if value > 2**32:
                raise ValueError("L'entier stocké dans la liste doit être un entier sous forme d'un hexadécimal contenant 8 bits")


    combine = 0
    for value in state:
        combine = combine << 32 | value
    
    return combine


def SwapColumnRow(state):

    """
    Inverse les colonnes avec les lignes d'un état.
    La liste doit être une liste de taille 4, contenant des entiers équivalent à un hexadécimal de 8 bits ou moins.

    Entrée : List[Int]
    Sortie : List[Int]

    Exemple : [0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f] -> [0x0004080c, 0x105090d, 0x2060a0e, 0x3070b0f]
    Affichage : 00 04 08 0c ->  00 01 02 03 
                01 05 09 0e     04 05 06 07
                02 06 0a 0d     08 09 0a 0b
                03 07 0b 0f     0c 0d 0e 0f
    """

    if type(state) != list:
        raise TypeError("Le type en entrée doit être une liste")
    elif len(state) != 4:
        raise ValueError("La liste doit posséder 4 valeurs")
    else:
        for value in state:
            if value > 2**32:
                raise ValueError("L'entier stocké dans la liste doit être un entier sous forme d'un hexadécimal contenant 8 bits")

    rows = []
    adapt = [[value >> (24 - i*8) & 0xff for value in state] for i in range(4)]

    for row in adapt:
        result_row = 0
        for value in row:
            result_row = result_row << 8 | value
        
        rows.append(result_row)

    return rows


def MixColumnCalcul(column):

    """
    Effectue les calculs pour un MixColumn.
    L'entrée est un entier équivalent à un hexadécimal de 8 bits, cette entier est une colonne de l'état.

    Entrée : Int
    Sortie : Int

    La fonction utilise des listes contenant le résultat des différents multiplications à utiliser durant le MixColumn.

    Exemple : 0x00010203 -> 0x02070005
    """
    
    if type(column) != int:
        raise TypeError("L'entrée doit être un entier")
    elif column > 2**32:
        raise ValueError("L'entier doit être un entier sous forme d'un hexadécimal contenant 8 bits")

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


def MixColumnReverseCalcul(column):

    """
    Effectue les calculs pour un MixColumn inversé afin de retrouver l'entier avant le MixColumn.
    L'entrée est un entier équivalent à un hexadécimal de 8 bits, cette entier est une colonne de l'état.

    Entrée : Int
    Sortie : Int

    La fonction utilise des listes contenant le résultat des différents multiplications à utiliser durant le MixColumn inversé.
    
    Exemple : 0x02070005 -> 0x00010203
    """

    if type(column) != int:
        raise TypeError("L'entrée doit être un entier")
    elif column > 2**32:
        raise ValueError("L'entier doit être un entier sous forme d'un hexadécimal contenant 8 bits")

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

    """
    Effectue un XOR entre l'état et la clé passée en argument.
    Les entrées sont un état, qui une liste de 4 entiers, et un entier, équivalent à un hexadécimal de 32 bits.
    
    Entrée : List[Int], Int
    Sortie : List[Int]
    
    Exemple : [0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f], 0x0102030405060708090a0b0c0d0e0f -> [0x0, 0x0, 0x0, 0x0]
    """

    if type(state) != list:
        raise TypeError("Le type en entrée doit être une liste")
    elif len(state) != 4:
        raise ValueError("La liste doit posséder 4 valeurs")
    else:
        for value in state:
            if value > 2**32:
                raise ValueError("L'entier stocké dans la liste doit être un entier sous forme d'un hexadécimal contenant 8 bits")

    if roundKey > 2**128:
        raise ValueError("L'entrée est supérieur à un hexadécimal contenant 32 bits.")

    word = CombineState(state)
    result = CreateState(word ^ roundKey)

    return result