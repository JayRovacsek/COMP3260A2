import unittest
import des0
# To run this unit test, run; python -m unittest test_feistal

class TestDESMethods(unittest.TestCase):

    def test_encrypt(self):
        # Test Encryption is applied
        self.assertNotEqual(plain_text,cipher_text,'Unit test failed; {}'.format(self.__module__))

    def test_decrypt(self):
        # Test Encryption is applied
        self.assertNotEqual(plain_text,cipher_text,'Unit test failed; {}'.format(self.__module__))

if __name__ == '__main__':
    unittest.main()