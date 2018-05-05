# the des0 function script
# since: 02-MAY-2018
# TODO: e-table, s-box, p-box : the tables of values, make them fast using numpy.array()
# the inputs will already be in binary form
import numpy as np
import json

class des:
    def __init__(self, key):
        self.key = key
        self.permute(1) # permute key as PC-1
        self.c = self.key[:int(len(self.key)/2)]
        self.d = self.key[int(len(self.key)/2):]
    
    def import_json(self,data_file):
        with open(data_file, encoding='utf-8') as f:
            return json.loads(f.read())

    def round(self, text):
        e_text = self.expand(text) # use the ebox
        self.gen_key() 
        result = self.key ^ e_text
        result = self.substitute(result) # use the sbox
        return result

    def pad_text(self,text,hex):
        if not hex:
            for c in text:
                hexstring += c.encode("hex")
            #self.plaintext = 
    
    def expand(self, text): # input text into an e-box
        result = self.shuffle('ebox.json', text)
        return result

    def substitute(self, input): # parse the text through the s-box
        out = "" # sub input into out
        return out

    def permute(self, num): # permute the key
        if num is 1:
            self.key = self.shuffle('PC-1.json', self.key)
        else:
            self.key = self.shuffle('PC-2.json', self.key)

    def shuffle(self, filename, text): 
        # shuffle the text based on information in the json return shuffled text
        shuffleText = ""
        shuffle_dict = self.import_json('PC-1.json')
        for key,value in shuffle_dict.items():
            shuffleText += text[value:value+1]

    def gen_key(self): # this is unfinished but still doesn't seem right yet
        shift = 2
        bit_num = len(self.c)
        for i in range(bit_num-shift, bit_num):
            c_shift = self.c[i:i+1]
            d_shift = self.d[i:i+1]
        for i in range(0, bit_num-shift):
            c_shift = c_shift + self.c[i:i+1]
            d_shift = d_shift + self.d[i:i+1]

    def end(self):
        self.permute(2) # permute key as PC-2
        return self.key
