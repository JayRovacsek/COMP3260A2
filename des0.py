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
        result = self.key ^ e_text
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

    def end(self):
        self.permute(2) # permute key as PC-2
        return self.key

# Text substitution functions
def substitute(inText): # parse the text through the s-box
    n = 6 # number of bytes the input is split into
    splitText = [inText[i:i+n] for i in range(0, len(inText), n)]
    for i in range(0,7):
        row = splitText[i][0] + splitText[i][len(splitText[i])-1]
        column = splitText[i][1:len(splitText[i])-2]
        # next retrieve numbers from s-box

    out = "" # sub input into out
    return out

def expand(text): # input text into an e-box
    result = shuffle('ebox', text)
    return result

def shuffle(filename, text):
    # shuffle the text based on information in the json, return shuffled text
    filename += ".arr"
    shuffleText = ""
    with open(filename, "r") as f:
        string = f.read()
        shuffleOrder = string.split(" ")
    for i, value in enumerate(shuffleOrder, 0):
        if value.endswith("\n"):
            shuffleOrder[i] = value[0:len(value)-2] # remove newlines
        curIndex = int(shuffleText[i])
        shuffleText += text[curIndex:curIndex+1]
    return shuffleText
