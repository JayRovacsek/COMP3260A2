# Script For a Feistal Block cipher, requires a Function.{Cipher,Decipher}
# Modified: 03-MAY-2018
# Author: Cody Lewis & Jay Rovacsek
# Since: 02-MAY-2018

# The Feistal block cipher Function
# param text - the [plain|cipher]text
# return - plaintext if ciphertext in, else ciphertext
import traceback
import sys
import desclass
import binascii

def cipher(text,key):
    des = desclass.des()
    if len(key)%64 is not 0:
        print('Key: {} was not 64 bits, now padding with 0\'s\nNew key: {} '.format(key,key.ljust(64,'0')))
        des.key = key.ljust(64,'0')
    else:
        des.key = key
    setattr(des,'c',32)
    setattr(des,'d',32)

    new_subkey = ""
    for i in range(0,15):
        for j in range(1,64):
            if j % 8 is not 0:
                new_subkey += key[des.PC1[str(j)]] # FIX ME 
    print(new_subkey)

    #     des.subkeys[i] = new_subkey
    # l_cur, r_cur = r_cur, l_cur
    # result = join_text(l_cur, r_cur)
    # key = FBox.end()
    # return result,key
    return None

# Initial Split of the [plain|cipher]text
# param plaintext - the [plain|cipher]text used at the beginning of the cipher
# return - the left and right halves of the plaintext
def split_text(text):
    return text[:int(len(text)/2),int(len(text)/2):]

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
    
    # This portion of code is only to debug with 
    args = ['-e','Alternate/testfile']
    if args[0] == '-e' or args[0] == '--encrypt':
        values = parse_file(args[1])
        if len(values) is not 0:
            print("Encrypting using:\nKey: {}\nPlaintext: {}".format(values['P'],values['K']))
            cipher(values['P'],values['K'])
    elif args[0] == '-d' or args[0] == '--decrypt':
        values = parse_file(args[1])
        if len(values) is not 0:
            print("Decrypting using:\nKey: {}\nPlaintext: {}".format(values['P'],values['K']))
            cipher(values['P'],values['K'])

    # if len(sys.argv) is 3:
    #     args = sys.argv
    #     del args[0]
    #     if args[0] == '-e' or args[0] == '--encrypt':
    #         values = parse_file(args[1])
    #         if len(values) is not 0:
    #             print("Encrypting using:\nKey: {}\nPlaintext: {}".format(values['P'],values['K']))
    #             cipher(values['P'],values['K'])
    #     elif args[0] == '-d' or args[0] == '--decrypt':
    #         values = parse_file(args[1])
    #         if len(values) is not 0:
    #             print("Decrypting using:\nKey: {}\nPlaintext: {}".format(values['P'],values['K']))
    #             cipher(values['P'],values['K'])
    #     else:
    #         print("An expected encrypt/decrypt flag was not found, please refer to the README.md\n" +
    #         "For encryption use the -e/--encrypt flag, eg;\n\"feistal.py -e testfile\" OR \"feistal.py --encrypt testfile\"" +
    #         "\nFor decryption please use the -d/--decrypt flag eg;\n\"feistal.py -d testfile\" OR \"feistal.py --decrypt testfile\"")
    # else:
    #     print("Length of arguments was not sufficient, please refer to the README.md")