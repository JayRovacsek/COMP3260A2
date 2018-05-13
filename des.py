# the des function script
# since: 02-MAY-2018
# TODO: make code neat, avalanche effect, output, decryption
# the inputs will already be in binary form
import os
import traceback
import sys

class des:
    def __init__(self, key, mode): # instantiate store key and set mode
        self.original_key = key
        key = pad_key(key)
        self.key = key
        self.permute1() # permute key as PC-1
        self.c = self.key[:int(len(self.key)/2)]
        self.d = self.key[int(len(self.key)/2):]
        self.round = 1
        self.subkeys = {}
        self.mode = mode
        self.generate_subkeys()

    # encrypt plaintext
    # return cipher text with final swap and key in tuple
    def encrypt(self, text):
        text = shuffle('IP', text)
        left_text = text[:int(len(text)/2)]
        right_text = text[int(len(text)/2):]
        for i in range(0, 16):
            left_text, right_text = self.round_fun(left_text, right_text)
        text = shuffle('IPinverse', right_text + left_text)
        try:
            with open(os.getcwd()+"/Results/encrypt.results",'w', encoding='utf-8') as f:
                f.write(text + "\n")
                f.write(self.original_key)
                print("File saved to: {}/Results/encrypt.results".format(os.getcwd()))
        except Exception:
            print("An error occurred: {}".format(traceback.format_exc()))
        for k in self.subkeys:
            print(self.subkeys[k])
        return text, self.original_key

    def decrypt(self, text):
        text = shuffle('IP', text)
        left_text = text[:int(len(text)/2)]
        right_text = text[int(len(text)/2):]
        for i in range(0, 16):
            left_text, right_text = self.round_fun(left_text, right_text)
        text = shuffle('IPinverse', right_text + left_text)
        try:
            with open(os.getcwd()+"/Results/decrypt.results",'w', encoding='utf-8') as f:
                f.write(text + "\n")
                f.write(self.original_key)
                print("File saved to: {}/Results/decrypt.results".format(os.getcwd()))
        except Exception:
            print("An error occurred: {}".format(traceback.format_exc()))
        for k in self.subkeys:
            print(self.subkeys[k])
        return text, self.original_key

    def round_fun(self, left_text, right_text): # a round of the des encryption
        print("Round {}, left: {}, right: {}".format(self.round, left_text, right_text))
        e_text = expand(right_text) # use the ebox
        print("expansion text: {}".format(e_text))
        # cur_key = self.subkeys[str(self.round)]
        # print("round key: ", cur_key)
        if self.mode == "encrypt":
            result = xor(self.subkeys[str(self.round)], e_text)
        else:
            result = xor(self.subkeys[str(17-self.round)], e_text)
        print("xor text: {}".format(result))
        result = substitute(result, self.mode) # use the sbox
        print("subbed text: {}".format(result))
        result = shuffle('P', result) # permute text
        print("Permuted text: {}".format(result))
        result = xor(result, left_text)
        print("xored with left: {}".format(result))

        self.round += 1
        left_text = right_text
        right_text = result
        print("Result: {}, {}".format(left_text, right_text))
        return left_text, right_text

    def permute1(self): # permute the key
        self.key = shuffle('PC-1', self.key)

    def generate_subkeys(self):
        shift_order = import_json('shift.json')
        c = self.c
        d = self.d
        for k in range(1,17):
            shift = shift_order[str(k)]
            c_shift, d_shift = "",""
            for i in range(shift, len(c)):
                c_shift += c[i:i+1]
                d_shift += d[i:i+1]
            for i in range(0, shift):
                c_shift += c[i:i+1]
                d_shift += d[i:i+1]
            c = c_shift
            d = d_shift
            self.subkeys[str(k)] = shuffle('PC-2', c + d)

    def gen_key(self): # shift the key
        shift_order = import_json('shift.json')
        shift = shift_order[str(self.round)]
        c_shift, d_shift = "",""
        for i in range(shift, len(self.c)):
            c_shift += self.c[i:i+1]
            d_shift += self.d[i:i+1]
        for i in range(0, shift):
            c_shift += self.c[i:i+1]
            d_shift += self.d[i:i+1]
        self.c = c_shift
        self.d = d_shift
        return self.permute2()

    def permute2(self):
        return shuffle('PC-2', self.c + self.d)

# Text substitution functions
def substitute(inText,mode): # parse the text through the s-box
    n = 6 # number of bytes the input is split into
    split_text = [inText[i:i+n] for i in range(0, len(inText), n)]
    s_box = [import_json("s1.json"), import_json("s2.json"), import_json("s3.json"),
             import_json("s4.json"), import_json("s5.json"), import_json("s6.json"),
             import_json("s7.json"), import_json("s8.json")]
    out = "" # sub input into out
    for i in range(0, 8):
        # next retrieve numbers from s-box
        add = bin(s_box[i][split_text[i]])[2:] # the substitution piece
        while len(add) < 4: # retain 4 bits per box
            add = "0" + add
        out += add
    return out

def expand(text): # input text into an e-box
    result = shuffle('ebox', text)
    return result

def import_json(data_file): # import a json and return a dictionary
    import json
    with open(data_file, encoding='utf-8') as f:
        return json.loads(f.read())

def shuffle(filename, text): # shuffle the text in accordance to a json file
    shuffle_text = ""
    shuffle_dict = import_json(filename + ".json")
    for key, value in shuffle_dict.items():
        shuffle_text += text[value-1 : value]   
    return shuffle_text

def xor(key, text): # XOR strings containing binary together
    result = ""
    text = text.zfill(len(key))
    for k, t in zip(key,text):
        result += str(int(k) ^ int(t))
    return result

def pad_key(key): # pads the key using even parity calculations
    if len(key) == 56:
        split_key = [key[i: i+7] for i in range(0, len(key), 7)]
        for i in range(0, len(split_key)):
            bit_count = 0
            for j in range(0, len(split_key[i])):
                if split_key[i][j] == "1":
                    bit_count += 1
            if (bit_count % 2) is 0:
                parity = "0"
            else:
                parity = "1"
            split_key[i] += parity
        return "".join(split_key)
    else:
        return key # in other cases there is no way of calculating parity