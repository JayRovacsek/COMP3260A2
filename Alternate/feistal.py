# Script For a Feistal Block cipher, requires a Function.{Cipher,Decipher}
# Modified: 03-MAY-2018
# Author: Cody Lewis & Jay Rovacsek
# Since: 02-MAY-2018

# The Feistal block cipher Function
# param text - the [plain|cipher]text
# return - plaintext if ciphertext in, else ciphertext
import traceback
import sys
#import des0
import binascii

def cipher(text,key):
    FBox = des0.des(key)
    l_cur, r_cur = split_text(text)
    for i in range(0,15):
        l_cur, r_cur = round(FBox, l_cur, r_cur)
    l_cur, r_cur = r_cur, l_cur
    result = join_text(l_cur, r_cur)
    key = FBox.end()
    return result,key

# Initial Split of the [plain|cipher]text
# param plaintext - the [plain|cipher]text used at the beginning of the cipher
# return - the left and right halves of the plaintext
def split_text(plain_text):
    l_init = plain_text[:int(len(plain_text)/2)]
    r_init = plain_text[int(len(plain_text)/2):]
    return l_init, r_init

# Join the two halves of the text at the end
# param l - the left half of the text
# param r - the right half of the text
# return - a concatonation of the left and right halves of the text
def join_text(l_fin, r_fin):
    return l_fin + r_fin

# A round of the [en|de]cryption process
# param lin - the left side of the text to go in
# param rin - the right side of the text
# return - the two halves of the [en|de]ciphered text
def round(FBox, lin, rin):
    lout = rin
    rout = FBox.cipher(rin) ^ lin
    return lout, rout

def parse_file(file):
    values = {}
    try:
        with open(file) as f:
            for line in f:
                if 'P' not in values:
                    values['P'] = line.replace("\n","")
                elif 'K' not in values:
                    values['K'] = line.replace("\n","")
                else:
                    print(line)
    except FileNotFoundError:
        print("You may have spelt the filename incorrectly, or the file doesn't exist.\nPlease try again")
        return None
    finally:
        return values

if __name__ == "__main__":
    if len(sys.argv) is 3:
        args = sys.argv
        del args[0]
        if args[0] == '-e' or args[0] == '--encrypt':
            values = parse_file(args[1])
            if len(values) is not 0:
                print("Encrypting using:\nKey: {}\nPlaintext: {}".format(values['P'],values['K']))
        elif args[0] == '-d' or args[0] == '--decrypt':
            values = parse_file(args[1])
            if len(values) is not 0:
                print("Decrypting using:\nKey: {}\nPlaintext: {}".format(values['P'],values['K']))
        else:
            print("An expected encrypt/decrypt flag was not found, please refer to the README.md\n" +
            "For encryption use the -e/--encrypt flag, eg;\n\"feistal.py -e testfile\" OR \"feistal.py --encrypt testfile\"" +
            "\nFor decryption please use the -d/--decrypt flag eg;\n\"feistal.py -d testfile\" OR \"feistal.py --decrypt testfile\"")
    else:
        print("Length of arguments was not sufficient, please refer to the README.md")