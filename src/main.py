import settings

from tools import ConvMsgKey, Hex32ToAscii
from encrypt import Encrypt
from decrypt import Decrypt
from square import Square4

import argparse

def print_state_like(state):
    if type(state) == int:
        if state > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
        
        combine = state
    else:
        raise TypeError("L'affichage ne prend en compte seulement un entier sous forme d'un hexadécimal contenant 32 bits.")

    state = []
    for i in range(120, -1, -8):
        state.append(combine >> i & 0xff)
    
    num_row = 4
    num_column = 4
    matrix = [[hex(state[i * num_row + j])[2:] for i in range(num_row)] for j in range(num_column)]

    print('\n'.join([''.join(['{:3}'.format(item.zfill(2)) for item in row]) for row in matrix]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="AES128", description="AES128 : Chiffrement / Déchiffrement / Attaque intégral AES128(4).", usage='main.py {encrypt,decrypt,attack} message clé (si chiffrement ou déchiffrement)\n\nLe mode "attack" nécessite une modification manuelle de la variable "secret_key" dans le fichier "settings.py".')

    subparsers = parser.add_subparsers(dest="actions", required=True)

    parser_encrypt = subparsers.add_parser('encrypt', help='Chiffrement du message avec une clé')
    parser_encrypt.add_argument('--ascii', '-as', help="Conversion du résultat en ASCII", action='store_true')
    parser_encrypt.add_argument('message', help="Message à chiffrer")
    parser_encrypt.add_argument('key', help="Clé à utiliser")

    parser_decrypt = subparsers.add_parser('decrypt', help='Déchiffrement du message avec une clé')
    parser_decrypt.add_argument('--ascii', '-as', help="Conversion du résultat en ASCII", action='store_true')
    parser_decrypt.add_argument('message', help="Message à déchiffrer")
    parser_decrypt.add_argument('key', help="Clé à utiliser")

    subparsers.add_parser('attack', help='Attaque intégral')

    args = parser.parse_args()

    match args.actions:
        case "encrypt":
            message, key = ConvMsgKey(args.message, args.key)
            result = Encrypt(message, key)

            print("Chiffrement:", result)
            if args.ascii:
                print("ASCII:", Hex32ToAscii(int(result, 16)))

        case "decrypt":
            message, key = ConvMsgKey(args.message, args.key)
            result = Decrypt(message, key)

            print("Déchiffrement:", result)
            if args.ascii:
                print("ASCII:", Hex32ToAscii(int(result, 16)))

        case "attack":
            settings.init()
            result = Square4()
            
            print(result)
            
        case _:
            raise ValueError()