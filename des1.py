import des
class des1(des.des):
    def round_fun(self, left_text, right_text):
        result = des.expand(right_text)
        result = des.substitute(result, self.mode)
        result = des.xor(result, left_text)
        return right_text, result
