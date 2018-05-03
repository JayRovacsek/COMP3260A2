# the des0 function script
# since: 02-MAY-2018
# TODO: e-table, s-box, p-box : the tables of values, make them fast using numpy.array()
import numpy as np
import json
class des:
    def __init__(self, key):
        self.key = key
        self.permute(1) # permute key as PC-1
        self.c = self.key[:int(len(self.key)/2)]
        self.d = self.key[int(len(self.key)/2):]

    def round(self, text):
        e_text = self.expand(text) # use the ebox
        self.gen_key() 
        result = self.key ^ e_text
        result = self.substitute(result) # use the sbox
        return result
    
    def expand(self, text):
        # input text into an e-box
        # return result
        with open('ebox.json','r'):
            ebox_table = json.load(f)
        
        result = text
        return result

    def substitute(self, input):
        out = "" # sub input into out
        return out

    def permute(self, num):
        if num is 1:
            return # permute key through PC-1
        else:
            return # premute key through PC-2

    def gen_key(self): # this is unfinished but still doesn't seem right yet
        shift = 2
        bit_num = len(self.c)
        c_bits = ""
        d_bits = ""
        for i in range(0, bit_num):
            c_bits += bin(ord(self.c[i:i+1]))[2:]
            d_bits += bin(ord(self.d[i:i+1]))[2:]
        for i in range(len(c_bits)-shift, len(c_bits)):
            c_shift = c_bits[i:i+1]
            d_shift = d_bits[i:i+1]
        for i in range(0, len(c_bits)-shift):
            c_shift = c_shift + c_bits[i:i+1]
            d_shift = d_shift + d_bits[i:i+1]

    def end(self):
        self.permute(2) # permute key as PC-2
        return self.key
