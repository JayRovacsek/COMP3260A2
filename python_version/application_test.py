import unittest
import pyDes
import random
import sys
from application import test_encryption, test_decryption

class TestDES(unittest.TestCase):
    def test_implentation(self):
        key = '00010010011010010101101111001001101101111011011111111000'
        encrypted_string = test_encryption('0000000100100011010001010110011110001001101010111100110111101111',key)[0]
        decrypted_string = test_decryption('1000010111101000000100110101010000001111000010101011010000000101',key)[0]
        self.assertNotEqual(encrypted_string,decrypted_string)
        self.assertEqual(encrypted_string,'1000010111101000000100110101010000001111000010101011010000000101')
        self.assertEqual(decrypted_string,'0000000100100011010001010110011110001001101010111100110111101111')

    def test_against_pydes(self):
        test_str_binary = '01110100011001010111001101110100011100110111010001110010'
        for i in range(0,100):
            word = ''
            while len(word) != 8:
                with open('test_files/dict.dat',mode='r') as f:
                    word = random.choice(f.readlines()).replace('\n','')
                    bytes_key = word[:8].encode('utf-8')
                    if len(word) >= 8:
                        word = word[:8]
                        print("Testing against seed: {}".format(word))
            des = pyDes.des(bytes_key)
            binary_key = bin(int.from_bytes(bytes_key, byteorder=sys.byteorder))[2:]
            pydes_ciphertext = des.encrypt('teststr'.encode('utf-8'),'0')
            pydes_binary_ciphertext = bin(int.from_bytes(pydes_ciphertext, byteorder=sys.byteorder))
            binary_ciphertext = test_encryption(test_str_binary,binary_key)[0]
            self.assertEqual(pydes_binary_ciphertext[2:],binary_ciphertext)