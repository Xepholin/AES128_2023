from constants import SBOX
import settings

from tools import StrToHex32, Rotword, Subword, Rcon
from encrypt import EncryptWithRounds


def SubByteInverse(byte):

    """
    Substitution inverse des caractères d'un entier, équivalent à un hexadécimal contenant 8 bits ou moins, en fonction de la table de substitution.

    Entrée : Int
    Sortie : Int

    La fonction scinde le byte en 2 parties de taille 4 bits, trouve la valeur de l'indice ligne et colonne dans la table.
    La valeur a cherché est trouvé avec l'aide des 4 premiers bits et les 4 derniers de l'entier scindé, où la 1ère correspond aux lignes et la 2e correspond aux colonnes.
    Fusionne ensuite toutes les partie qui ont été substitué.

    Exemple : 0x7c -> 0x01
    """

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


def CreateDelta(key, delta_position):

    """
    Génère une liste de message chiffré avec la même clé en fonction de la position qui a été donnée en entrée.

    Entrée : Int|Str, Int
    Sortie : List[Int][256]

    Une liste est d'abord rempli avec des entiers (de 0 à 255) tous à la même position dans leur représentation en hexadécimal.
        XX 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
    Dessiner sous forme d'état pour la compréhension.
    Ici en position 0 où XX est tous les entiers entre 00 et FF, les emplacements restantes sont constitués de 0.
    Ensuite tous ses états sont chiffrés avec l'AES128 sur 4 tours pour être à la fin ajouter dans une nouvelle liste.
    Cette liste contenant les états chiffrés est renvoyée à la fin de la fonction.
    """

    if type(key) == str:
        key = StrToHex32(key)
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
        encrypted = int(EncryptWithRounds(delta, key, 4), 16)
        delta_enc.append(encrypted)
    
    return delta_enc


def ReverseState(key_guess, position, delta_set):

    """
    Génère une liste contenant la version de l'état à la fin du tour 3.

    Entrée : Int, Int, List[Int][X]
    Sortie : List[Int][X]

    Afin de reconstituer la version de l'état au tour 3, nous devons pour chaque entier du delta_set:
        - isoler le byte actif
        - effectue un XOR entre le byte actif et key_guess
        - faire une subtsitution inversée du résultat du XOR
    Le résultat des opérations de chaque entier du delta_set est ajouté dans une nouvelle liste qui est renvoyé à la fin de la fonction.
    """

    reverse_set = []

    for state in delta_set:
        byte = state >> (15 - position) * 8 & 0xff
        byte ^= key_guess
        byte = SubByteInverse(byte)
        
        reverse_set.append(byte)

    return reverse_set


def CheckKeyGuess(reversed_bytes):

    """
    Retourne True ou False en fonction du résultat du XOR de tous les bytes dans la liste donnée en entrée.

    Entrée : Liste[Int]
    Sortie : Bool

    XOR chaque bytes de reversed_bytes entre eux, si le résultat est égal à 0, retourne True, sinon False.
    """

    result = 0

    for byte in reversed_bytes:
        result ^= byte

    return result == 0


def search_subKey4(delta_set):

    """
    Pour chaque éléments de la liste en entrée, trouve les bytes de toutes les positions entre 0 et 16, qui ont réussit à passer le CheckKeyGuess.

    Entrée : Liste[Int]
    Sortie : List[Liste[Int]][16]

    La fonction génère 16 listes, par rapport au delta_set, contenant les bytes actifs avec une position différente pour chacune d'entre eux.
    Tout d'abord, nous devons effectuer 16 opérations correspondant aux 16 parties de la clé.
    Pour chaque partie de la clé, on effectue un retour vers la version de la fin du tour 3 de l'AES avec toutes les valeurs possibles en utilisant la fonction ReverseState.
    Toutes les valeurs possibles, qu'on appelera byte hypothétique, sont des bytes recouvrent les valeurs entre 0x00 et 0xFF,
    Chaque liste contenant les 256 bytes est passé à la fonction CheckKeyGuess pour vérifier si le XOR de tous les éléments est égal à 0.
    Si c'est le cas, alors le byte qui hypothétique est ajouté à une liste.
    Cette liste L2 est contenu dans une autre liste L1, ou la L1[L2] correspond à la position choisie.
    On se retrouve alors avec une liste, contenant 16 listes, qui possèdent chacunes des entiers, qui ont réussi à passer l'égalité.
    """

    guess = [set() for _ in range(16)]
    
    for i in range(16):
        for j in range(256):
            reverse_set = ReverseState(j, i, delta_set)

            if CheckKeyGuess(reverse_set):
                guess[i].add(j)
    
    return guess

def secret_enc_delta(position):

    """
    Créer un delta_set avec la clé secrète contenue dans le fichier settings.py, avec la position passée en entrée.

    Entrée : Int
    Sortie : List[Int][256]
    """

    return CreateDelta(settings.secret_key, position)


def find_subKey4():

    """
    Trouve la sous-clé du tour 4 en fonction de la clé secrète contenue dans le fichier settings.py.

    Entrée :
    Sortie : Int

    Afin de trouver la sous-clé du tour 4, nous devons vérifier l'égalité XOR de tous les valeurs du delta_set chiffrés, pour en déterminer les bytes de la clé recherchée.
    On va d'abord commencé par essayer de trouver les bytes de la clé en utilisant la position 0 pour générer le delta_set chiffré.
    Si nous avons exactement 1 byte trouvé pour chaque partie de la clé, nous avons donc trouvé la clé recherchée.
    Si nous avons plus d'un byte trouvé pour chaque partie, nous devons alors effectuer une autre recherche de byte mais avec un delta_set chiffré avec une position différente.
    Nous faisons une intersection entre les bytes trouvés précédements et les nouveaux afin de réduire le nombre de byte pour chaque position.
    Cette opération peut être effectué au maximum 15 fois, car il n'y a que 16 positions possibles dans la clé, si nous utilisons des delta_set avec 1 byte de modifier 32/2 = 16.
    Quand il y a exactement 1 byte trouvé pour chaque partie de la clé, nous arrêtons la boucle, on fusionne chaque partie pour constituer la clé, puis nous renvoyons cette clé.
    """

    result = 0
    previous_guess = search_subKey4(secret_enc_delta(0))

    for i in range(1, 17):      # Boucle jusqu'à 17, pour gérer l'erreur où il n'y a toujours pas de clé trouvée alors que toutes les positions ont été utilisé
        delta_set = secret_enc_delta(i)
        guess = search_subKey4(delta_set)

        count = 0
        for j in range(16):
            guess[j] = guess[j] & previous_guess[j]

            if len(guess[j]) == 1:
                count += 1
        
        if count == 16:
            break

        previous_guess = guess

    guess = [byte.pop() for byte in guess]

    for guess_byte in guess:
        result = result << 8 | guess_byte

    return result


def InvertKeyScheduler(round, key):

    """
    Retrouve la clé maître avec la sous-clé donnée en entrée et le tour de la sous-clé donné en entrée.

    Entrée : Int|Str, Int
    Sortie : Int

    La clé en entrée peut être un entier, sous la forme d'un hexadécimal sur 32 bits ou moins, ou une chaîne de caractère représentant cet équivalent hexadécimal.
    La fonction consiste à effectuer les opérations inverses de l'expansion de clé pour retrouver la clé maître.
    """

    if type(key) == str:
        key = int(key, 16)
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


def Square4():

    """
    Effectue l'attaque carré sur l'AES128 à 4 tours avec la clé secrète présent dans le fichier settings.py.

    Entrée : 
    Sortie : Str

    La fonction appelle les fonctions find_subKeys4 et InvertKeyScheduler décrites précédement.
    Comme l'attaque est fait sur un AES à 4 tour, InvertKeyScheduler est donc utilisé avec 4 comme nombre de tours.
    """

    subKey4 = find_subKey4()
    masyerKey = InvertKeyScheduler(4, subKey4)

    return hex(masyerKey)[2:]

## Les fonctions en dessous sont pareilles que ceux du haut, mais elles prennent un paramètre en plus.
# Ce paramètre correspond à la clé maître (ou clé secrète, nommé dans les autres fonctions).
# Ses fonctions ont été crée et utiliser dans le but d'implémenter les tests unitaires.
# Sinon, pour répondre à la question,
# "Pourquoi ne pas avoir utilisé directement ses fonctions à la place de ceux du haut ?"
# C'est parce que je trouvais cela étrange d'effectuer l'attaque avec en entrée la clé maître à trouvé. 
def secret_enc_delta_test(key, position):
    return CreateDelta(key, position)


def find_subKey4_test(key):
    if type(key) == str:
        key = StrToHex32(key)
    if type(key) == int:
        if key > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
    else:
        raise TypeError("La clé doit être un hexadécimal sur 32 bits.")
    
    result = 0
    previous_guess = search_subKey4(secret_enc_delta_test(key, 0))

    for i in range(1, 100):
        delta_set = secret_enc_delta_test(key, i)
        guess = search_subKey4(delta_set)

        count = 0
        for i in range(16):
            guess[i] = guess[i] & previous_guess[i]

            if len(guess[i]) == 1:
                count += 1
        
        if count == 16:
            break

        previous_guess = guess

    guess = [byte.pop() for byte in guess]

    for guess_byte in guess:
        result = result << 8 | guess_byte

    return result


def Square4Test(key):
    subKey4 = find_subKey4_test(key)
    masterKey = InvertKeyScheduler(4, subKey4)

    return hex(masterKey)[2:]