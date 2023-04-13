from utilities import *
from encrypt import *

if __name__ == "__main__":
    word = 0x2b7e151628aed2a6abf7158809cf4f3c
    example = [0x2b7e151628aed2a6abf7158809cf4f3c, 0xa0fafe1788542cb123a339392a6c7605, 0xf2c295f27a96b9435935807a7359f67f, 0x3d80477d4716fe3e1e237e446d7a883b, 0xef44a541a8525b7fb671253bdb0bad00, 0xd4d1c6f87c839d87caf2b8bc11f915bc, 0x6d88a37a110b3efddbf98641ca0093fd, 0x4e54f70e5f5fc9f384a64fb24ea6dc4f, 0xead27321b58dbad2312bf5607f8d292f, 0xac7766f319fadc2128d12941575c006e, 0xd014f9a8c9ee2589e13f0cc8b6630ca6]

    test = "this is one text"
    key = 0x000102030405060708090a0b0c0d0e0f

    subkeys = KeyScheduler(key)

    state = create_state(key)
    print_state(state)
    print("-----------")
    state = ShiftRow(state)
    print_state(state)
    print("-----------")
    state = SubBytes(state)
    print_state(state)
    print("-----------")
    state = MixColumns(state)
    print_state(state)
    print("-----------")
    word = AddRoundKey(state, subkeys[1])
    print_state(word)