from tools import Hex32ToAscii

from encrypt import Encrypt
from decrypt import Decrypt
from square import Square4Test

import unittest
import random


class TestEncrypt(unittest.TestCase):

    def test_str_message(self):
        self.assertEqual(Encrypt("theblockbreakers", 0x2b7e151628aed2a6abf7158809cf4f3c), "c69f25d0025a9ef32393f63e2f05b747")

    def test_1(self):
        self.assertEqual(Encrypt(0x6bc1bee22e409f96e93d7e117393172a, 0x2b7e151628aed2a6abf7158809cf4f3c), "3ad77bb40d7a3660a89ecaf32466ef97")

    def test_2(self):
        self.assertEqual(Encrypt(0xae2d8a571e03ac9c9eb76fac45af8e51, 0x2b7e151628aed2a6abf7158809cf4f3c), "f5d3d58503b9699de785895a96fdbaaf")

    def test_3(self):
        self.assertEqual(Encrypt(0x30c81c46a35ce411e5fbc1191a0a52ef, 0x2b7e151628aed2a6abf7158809cf4f3c), "43b1cd7f598ece23881b00e3ed030688")

    def test_4(self):
        self.assertEqual(Encrypt(0xf69f2445df4f9b17ad2b417be66c3710, 0x2b7e151628aed2a6abf7158809cf4f3c), "7b0c785e27e8ad3f8223207104725dd4")


class TestDecrypt(unittest.TestCase):

    def test_str_message(self):
        self.assertEqual(Hex32ToAscii(int(Decrypt(0xc69f25d0025a9ef32393f63e2f05b747, 0x2b7e151628aed2a6abf7158809cf4f3c), 16)), "theblockbreakers")

    def test_1(self):
        self.assertEqual(Decrypt(0x3ad77bb40d7a3660a89ecaf32466ef97, 0x2b7e151628aed2a6abf7158809cf4f3c), "6bc1bee22e409f96e93d7e117393172a")

    def test_2(self):
        self.assertEqual(Decrypt(0xf5d3d58503b9699de785895a96fdbaaf, 0x2b7e151628aed2a6abf7158809cf4f3c), "ae2d8a571e03ac9c9eb76fac45af8e51")

    def test_3(self):
        self.assertEqual(Decrypt(0x43b1cd7f598ece23881b00e3ed030688, 0x2b7e151628aed2a6abf7158809cf4f3c), "30c81c46a35ce411e5fbc1191a0a52ef")

    def test_4(self):
        self.assertEqual(Decrypt(0x7b0c785e27e8ad3f8223207104725dd4, 0x2b7e151628aed2a6abf7158809cf4f3c), "f69f2445df4f9b17ad2b417be66c3710")

    def test_5(self):
        self.assertEqual(Decrypt(0x7b0c785e27e8ad3f8223207104725dd4, 0x2b7e151628aed2a6abf7158809cf4f3c), "f69f2445df4f9b17ad2b417be66c3710")


class TestSquare(unittest.TestCase):

    def test_1(self):
        masterKey = 0x2b7e151628aed2a6abf7158809cf4f3c

        self.assertEqual(Square4Test(masterKey), "2b7e151628aed2a6abf7158809cf4f3c")

    def test_2(self):
        masterKey = 0x000102030405060708090a0b0c0d0e0f

        self.assertEqual(Square4Test(masterKey), "102030405060708090a0b0c0d0e0f")

    def test_3(self):
        masterKey = 0x763979244226452948404D635166546A

        self.assertEqual(Square4Test(masterKey), "763979244226452948404d635166546a")

    def test_4(self):
        masterKey = random.randint(0, 2^128)
        self.assertEqual(Square4Test(masterKey), hex(masterKey)[2:])


if __name__ == "__main__":
    unittest.main()