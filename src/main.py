from utilities import *
from encrypt import *

if __name__ == "__main__":
    enc = encrypt("theblockbreakers", 0x2b7e151628aed2a6abf7158809cf4f3c)

    if enc == 0xc69f25d0025a9ef32393f63e2f05b747:
        print("valid")
        print("-----------")
        print_state_like(enc)
        print("-----------")
        print(HeSt_to_ascii(enc))
    else:
        print("false")
        print_state_like(enc)