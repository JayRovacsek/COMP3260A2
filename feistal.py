# Script For a Feistal Block cipher, requires a Function.{Cipher,Decipher}
# Author: Cody Lewis
# Since: 02-MAY-2018

# The Feistal block cipher Function
# param text - the [plain|cipher]text
# return - plaintext if ciphertext in, else ciphertext
def cipher(text):
    l_cur, r_cur = split_text(text)
    for i in range(0,15):
        l_cur, r_cur = round(l_cur, r_cur)
    l_cur, r_cur = r_cur, l_cur
    result = join_text(l_cur, r_cur)
    return result

# Initial Split of the [plain|cipher]text
# param plaintext - the [plain|cipher]text used at the beginning of the cipher
# return - the left and right halves of the plaintext
def split_text(plain_text):
    l_init = plain_text[:int(len(plain_text)/2)]
    r_init = plain_text[int(len(plain_text)/2):]
    return l_init, r_init

# Join the two halves of the text at the end
# param l - the left half of the text
# param r - the right half of the text
# return - a concatonation of the left and right halves of the text
def join_text(l_fin, r_fin):
    return l_fin + r_fin

# A round of the [en|de]cryption process
# param lin - the left side of the text to go in
# param rin - the right side of the text
# return - the two halves of the [en|de]ciphered text
def round(lin, rin):
    import des0 as FBox # this will need to be dependant on the specified des version
    lout = rin
    rout = FBox.cipher(rin) ^ lin
    return lout, rout
