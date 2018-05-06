# the des0 function script
# since: 02-MAY-2018
# TODO: s-box, testing
# the inputs will already be in binary form
class des:
    def __init__(self, key): # instantiate and store key
        self.key = key
        self.permute(1) # permute key as PC-1
        self.c = self.key[:int(len(self.key)/2)]
        self.d = self.key[int(len(self.key)/2):]

    def round(self, text):
        e_text = expand(text) # use the ebox
        self.gen_key()
        result = xor(self.key, e_text)
#        result = substitute(result) # use the sbox
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

    def end(self):
        self.permute(2) # permute key as PC-2
        return self.key

# Text substitution functions
def substitute(inText): # parse the text through the s-box
    n = 6 # number of bytes the input is split into
    splitText = [inText[i:i+n] for i in range(0, len(inText), n)]
    for i in range(0, 7):
        row = splitText[i][0] + splitText[i][len(splitText[i])-1]
        column = splitText[i][1:len(splitText[i])-2]
        # next retrieve numbers from s-box

    out = "" # sub input into out
    return out

def expand(text): # input text into an e-box
    result = shuffle('ebox', text)
    return result

def import_json(data_file):
    import json
    with open(data_file, encoding='utf-8') as f:
        return json.loads(f.read())

def shuffle(filename, text):
    shuffleText = ""
    shuffleDict = import_json(filename + ".json")
    for key, value in shuffleDict.items():
        shuffleText += text[value-1 : value]   
    return shuffleText

def xor(a, b):
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

if __name__ == "__main__": # test fn
    d = des("0000")
    print(d.round("1111111111111111111111111111"))
#    print(expand("abcdefghijklmnopqrstuvwxyzabcdef")) # expansion test
