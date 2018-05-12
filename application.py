import des
import sys

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
            _des = des.des(values['K'])
        if args[0] == '-e' or args[0] == '--encrypt':
            if len(values) is not 0:
                print("Encrypting using:\nKey: {}\nPlaintext: {}".format(values['P'],values['K']))
                print(_des.encrypt(values['P']))
        elif args[0] == '-d' or args[0] == '--decrypt':
            if len(values) is not 0:
                print("Decrypting using:\nKey: {}\nPlaintext: {}".format(values['P'],values['K']))
                print(_des.decrypt(values['P']))
        else:
            print("An expected encrypt/decrypt flag was not found, please refer to the README.md\n" +
            "For encryption use the -e/--encrypt flag, eg;\n\"application.py -e testfile\" OR \"application.py --encrypt testfile\"" +
            "\nFor decryption please use the -d/--decrypt flag eg;\n\"application.py -d testfile\" OR \"application.py --decrypt testfile\"")
    else:
        print("Length of arguments was not sufficient, please refer to the README.md")