# des.py - COMP3260A2
# the des function script
#
# Authors: Jay Rovacsek, Cody Lewis
# since: 02-MAY-2018
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
        return text, self.original_key

    def decrypt(self, text): # decrypt cipher text
        text = shuffle('IP', text)
        left_text = text[:int(len(text)/2)]
        right_text = text[int(len(text)/2):]
        for i in range(0, 16):
            left_text, right_text = self.round_fun(left_text, right_text)
        text = shuffle('IPinverse', right_text + left_text)
        return text, self.original_key

    def round_fun(self, left_text, right_text): # a round of the des encryption
        e_text = expand(right_text) # use the ebox
        if self.mode == "encrypt":
            result = xor(self.subkeys[str(self.round)], e_text)
        else:
            result = xor(self.subkeys[str(17-self.round)], e_text)
        result = substitute(result, self.mode) # use the sbox
        result = shuffle('P', result) # permute text
        result = xor(result, left_text)
        self.round += 1
        left_text = right_text
        right_text = result
        return left_text, right_text

    def permute1(self): # permute the key
        self.key = shuffle('PC-1', self.key)

    def generate_subkeys(self): # create each of thre subkeys
        shift_order = import_json('shift.json')
        c = self.c # the half key blocks
        d = self.d
        for k in range(1,17):
            shift = shift_order[str(k)] # shifts the keys
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

    def permute2(self): # permute the shifted half keys
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

def avalanche(text, key):
    text = shuffle('IP', text) # initial permutation
    text_perms = permute_text(text) # the list of possible texts
    key_perms = permute_text(key) # the list of possible keys
    result = avalanche_perm(text, key, text_perms, "text") + "\n"
    result += avalanche_perm(text, key, key_perms, "key")
    return result

def avalanche_perm(text, key, perms, perm_type):
    import des1
    import des2
    import des3
    mode = "encrypt" # assert in encryption mode
    result = ""
    k = 1
    diff_list = [[], [], [], []]
    for perm in perms: # iterate through permutations
        if perm_type == "text":
            result += "\nP and P{} under K\n".format(k)
        else:
            result += "\nP under K and K{}\n".format(k)
        k += 1
        result += "Round  DES0  DES1  DES2  DES3\n"
        deses = []
        if perm_type == "text":
            j = 2
        else:
            j = 1
        for i in range(0, j):
            deses.append([des(key, mode), des1.des1(key, mode),
                          des2.des2(key, mode), des3.des3(key, mode)])
        if perm_type == "key":
            deses.append([des(perm, mode), des1.des1(perm, mode),
                          des2.des2(perm, mode), des3.des3(perm, mode)])
        result += "    0"
        perm_left = []
        perm_right = []
        left_text = []
        right_text = []
        for i in range(0, 4):
            if perm_type == "text":
                p_text = perm
            else:
                p_text = text
            result += "   {}".format(text_diff(text, p_text))
            perm_left.append(p_text[:int(len(text)/2)])
            perm_right.append(p_text[int(len(text)/2):])
            left_text.append(text[:int(len(text)/2)])
            right_text.append(text[int(len(text)/2):])
        for i in range(0, 16): # the rounds of encryption
            result += "\n    {}".format(i + 1)
            for j in range(0, 4):
                perm_left[j], perm_right[j] = deses[0][j].round_fun(perm_left[j], perm_right[j])
                left_text[j], right_text[j] = deses[1][j].round_fun(left_text[j], right_text[j])
                diff = text_diff(left_text[j] + right_text[j], perm_left[j] + perm_right[j])
                result += "   {}".format(diff)
                if i == 15: # if last round
                    diff_list[j].append(diff)
    result += "\nAvg    "
    for j in range(0, 4):
        add = 0
        for diff in diff_list[j]:
            add += diff
        result += "{}   ".format(add / len(diff_list[j]))
    return result

def permute_text(text): # return a list of permutations of a given text
    result = []
    for i in range(0, len(text)):
        if text[i] == "1":
            add = "0"
        else:
            add = "1"
        result.append(text[:i] + add + text[i+1:])
    return result

def text_diff(text, delta_text):
    result = 0
    length = len(text) if len(text) <= len(delta_text) else len(delta_text)
    for i in range(length):
        if text[i] != delta_text[i]:
            result += 1
    return result
