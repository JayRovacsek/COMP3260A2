import sys
import traceback
import os
import des

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
                    break
    except FileNotFoundError:
        print("You may have spelt the filename incorrectly, or the file doesn't exist.\nPlease try again")
        return None
    finally:
        return values

if __name__ == "__main__":
    if len(sys.argv) is 3:
        args = sys.argv
        del args[0]
        values = parse_file(args[1])
        if len(values) is not 0:
            if args[0] == '-e' or args[0] == '--encrypt':
                _des = des.des(values['K'],"encrypt")
                print("Encrypting using:\nPlaintext P: {}\nKey K: {}".format(values['P'], values['K']))
                text, key = _des.encrypt(values['P'])
                print("Ciphertext C: {}".format(text))
                try:
                    with open(os.getcwd()+"/Results/encrypt.results",'w', encoding='utf-8') as f:
                        f.write("Plaintext P: {}\nKey K: {}\nCiphertext C: {}".format(values['P'], key, text))
                    print("The results were saved to: {}/Results/encrypt.results".format(os.getcwd()))
                except Exception:
                    print("An error occurred: {}".format(traceback.format_exc()))
            elif args[0] == '-d' or args[0] == '--decrypt':
                _des = des.des(values['K'],"decrypt")
                print("Decrypting using:\nCiphertext C: {}\nKey K: {}".format(values['P'], values['K']))
                text, key = _des.decrypt(values['P'])
                print("Plaintext P: {}".format(text))
                try:
                    with open(os.getcwd()+"/Results/decrypt.results",'w', encoding='utf-8') as f:
                        f.write("Ciphertext C: {}\nKey K: {}\nPlaintext P: {}".format(values['P'], key, text))
                    print("The results were saved to: {}/Results/decrypt.results".format(os.getcwd()))
                except Exception:
                    print("An error occurred: {}".format(traceback.format_exc()))
            else:
                print("An expected encrypt/decrypt flag was not found, please refer to the README.md\n" +
                "For encryption use the -e/--encrypt flag, eg;\n\"application.py -e testfile\" OR \"application.py --encrypt testfile\"" +
                "\nFor decryption please use the -d/--decrypt flag eg;\n\"application.py -d testfile\" OR \"application.py --decrypt testfile\"")
        else:
            print("You may have accidentally tried to use a file that did not have a key/text pair")
    else:
        print("Length of arguments was not sufficient, please refer to the README.md")
