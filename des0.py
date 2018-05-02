# the des0 function script
# since: 02-MAY-2018
# TODO: key generation, round function, e-table, s-box, permutation
class des:
    def __init__(self, key):
        self.key = key
        self.c = key[:int(len(key)/2)]
        self.d = key[int(len(key)/2):]

    def round(self, text):
        e_text = self.expand(text)
        self.key = self.genKey(self.c, self.d)
        result = self.key ^ e_text
        result = self.substitute(result)
        result = self.permute(result)
        return result
    
    def expand(self, text):
        # input text into an e-box
        # return result
        result = text
        return result

    def genKey(self, c, d): # this is unfinished but still doesn't seem right yet
        shift = 2
        bitNum = len(c)
        c_bits = 0
        d_bits = 0
        for i in range(0,bitNum):
            c_bits += ord(c[i:i+1])
            d_bits += ord(d[i:i+1])
        c_bits = c_bits << shift
        if(c_bits > 2**bitNum): # shift bit around the number
            return
        d_bits = d_bits << shift
