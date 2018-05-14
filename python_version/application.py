# application.py - COMP3260A2
# The main thread of the des program
#
# Authors: Jay Rovacsek, Cody Lewis
# Since: 12-MAY-2018
import sys
import traceback
import os
import des

def parse_file(file): # parse the input file
    values = {}
    try:
        with open(file) as f:
            for line in f:
                if 'T' not in values:
                    values['T'] = line.replace("\n","")
                elif 'P' not in values:
                    values['P'] = line.replace("\n","")
                elif 'K' not in values:
                    values['K'] = line.replace("\n","")
                else:
                    break
    except FileNotFoundError:
        print("You may have spelt the filename incorrectly, or the file doesn't exist.\nPlease try again")
        return None
    finally:
        return values

if __name__ == "__main__": # IO
    if len(sys.argv) is 3:
        args = sys.argv
        del args[0]
        values = parse_file(args[0]) # takes file input (2nd argument)
        if len(values) is not 0:
            if values['T'] == '0':
                _des = des.des(values['K'],"encrypt")
                print("Encrypting using:\nPlaintext P: {}\nKey K: {}".format(values['P'], values['K']))
                text, key = _des.encrypt(values['P'])
                print("Ciphertext C: {}".format(text))
                avalanche = des.avalanche(values['P'], values['K'])
                print("Avalanche:\n{}".format(avalanche))
                try: # file output
                    with open(args[1], 'w') as f:
                        f.write("ENCRYPTION\nPlaintext P: {}\nKey K: {}\nCiphertext C: {}\nAvalanche:\n{}".format(values['P'], key, text, avalanche))
                    print("The results were saved to: {}".format(args[1]))
                except Exception:
                    print("An error occurred: {}".format(traceback.format_exc()))

            elif values['T'] == '1':
                _des = des.des(values['K'],"decrypt")
                print("Decrypting using:\nCiphertext C: {}\nKey K: {}".format(values['P'], values['K']))
                text, key = _des.decrypt(values['P'])
                print("Plaintext P: {}".format(text))
                try:
                    with open(args[1], 'w') as f: # file output
                        f.write("DECRYPTION\nCiphertext C: {}\nKey K: {}\nPlaintext P: {}".format(values['P'], key, text))
                    print("The results were saved to: {}".format(args[1]))
                except Exception:
                    print("An error occurred: {}".format(traceback.format_exc()))
            else:
                print("An expected encrypt/decrypt flag was not found, please refer to the README.md\n" +
                "For encryption use put '0' at the top of the file " +
                "\nFor decryption please put '1' at the top of the file")
        else:
            print("You may have accidentally tried to use a file that did not have a key/text pair")
    else:
        print("Length of arguments was not sufficient, please refer to the README.txt")
