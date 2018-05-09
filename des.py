# the des0 function script
# since: 02-MAY-2018
# TODO: key generation/permutation
# the inputs will already be in binary form
class des:
    def __init__(self, key): # instantiate and store key
        key = pad_key(key)
        self.key = key
        self.permute(1) # permute key as PC-1
        self.c = self.key[:int(len(self.key)/2)]
        self.d = self.key[int(len(self.key)/2):]

    def round(self, text): # a round of the des encryption
        e_text = expand(text) # use the ebox
        self.gen_key() # needs fixing
        result = xor(self.c, e_text)
        result = e_text # this is only for testing
        result = substitute(result) # use the sbox
        return result

    def permute(self, num): # permute the key
        if num is 1:
            self.key = shuffle('PC-1', self.key)
        else:
            self.key = shuffle('PC-2', self.key)

    def gen_key(self): # shift the key
        shift = 2
        bit_num = len(self.c)
        for i in range(bit_num - shift, bit_num):
            c_shift = self.c[i:i+1]
            d_shift = self.d[i:i+1]
        for i in range(0, bit_num - shift):
            c_shift = c_shift + self.c[i:i+1]
            d_shift = d_shift + self.d[i:i+1]

    def end(self): # the final permutation of the key
        self.permute(2) # permute key as PC-2
        return self.key

# Text substitution functions
def substitute(inText): # parse the text through the s-box
    n = 6 # number of bytes the input is split into
    splitText = [inText[i:i+n] for i in range(0, len(inText), n)]
    s_box = [import_json("s1.json"), import_json("s2.json"), import_json("s3.json"),
             import_json("s4.json"), import_json("s5.json"), import_json("s6.json"),
             import_json("s7.json"), import_json("s8.json")]
    out = "" # sub input into out
    for i in range(0, 8):
        # next retrieve numbers from s-box
        add = bin(s_box[i][splitText[i]])[2:] # the substitution piece
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
    shuffleText = ""
    shuffleDict = import_json(filename + ".json")
    for key, value in shuffleDict.items():
        shuffleText += text[value-1 : value]   
    return shuffleText

def xor(a, b): # XOR strings containing binary together
    if len(a) > len(b):
        length = len(b)
        offset_a = len(a) - length
        offset_b = 0
    else:
        length = len(a)
        offset_a = 0
        offset_b = len(b) - length
    result = ""
    for i in range(0, length):
        if a[offset_a + i] == "1" and b[offset_b + i] == "1":
            result += "0"
        elif a[offset_a + i] == "1" or b[offset_b + i] == "1":
            result += "1"
        else:
            result += "0"
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

if __name__ == "__main__": # test fn
    d = des("0"*56)
    print(d.round("1"*32))
