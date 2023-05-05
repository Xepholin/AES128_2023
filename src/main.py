import settings

from tools import ascii_to_hex, hex32_to_ascii
from encrypt import encrypt
from decrypt import decrypt
from square import square4

import argparse

def print_state_like(state):
    if type(state) == int:
        if state > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
        
        combine = state
    else:
        raise TypeError("L'affichage ne prend en compte seulement une liste contenant les 4 partie de mots en hexadécimal ou un entier sur 32 bits.")

    state = []
    for i in range(120, -1, -8):
        state.append(combine >> i & 0xff)
    
    num_row = 4
    num_column = 4
    matrix = [[hex(state[i * num_row + j])[2:] for i in range(num_row)] for j in range(num_column)]

    print('\n'.join([''.join(['{:3}'.format(item.zfill(2)) for item in row]) for row in matrix]))


def parser_init():
    parser = argparse.ArgumentParser(prog="AES128", description="AES128 : Chiffrement / Déchiffrement / Attaque intégral AES128(4).", usage='main.py {encrypt,decrypt,attack} message clé (si chiffrement ou déchiffrement)\n\nLe mode "attack" nécessite une modification manuelle de la varaible "secret_key" dans le fichier "settings.py".')

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

    return parser

def conv_msg_key(message, key):
    if len(message) == 32:
        message = int(message, 16)
    if len(key) == 32:
        key = int(key, 16)

    if type(message) != int:
        if len(message) == 16:
            message = ascii_to_hex(message)
    if type(key) != int:
        if len(key) == 16:
            key = ascii_to_hex(key)
    
    return message, key

if __name__ == "__main__":
    settings.init()
    parser = parser_init()

    args = parser.parse_args()

    match args.actions:
        case "encrypt":
            message, key = conv_msg_key(args.message, args.key)
            result = encrypt(message, key)
            if args.ascii:
                result = hex32_to_ascii(int(result, 16))

        case "decrypt":
            message, key = conv_msg_key(args.message, args.key)
            result = decrypt(message, key)
            if args.ascii:
                result = hex32_to_ascii(int(result, 16))

        case "attack":
            result = square4()
            
        case _:
            raise ValueError()
        
    print(result)