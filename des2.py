# des2.py - COMP3260A2
# One of the variations of the des program
#
# Authors: Jay Rovacsek, Cody Lewis
# Since: 13-MAY-2018
import des
class des2(des.des):
    def round_fun(self, left_text, right_text):
        result = des.expand(right_text)
        result = des.shuffle('inverseEbox', result)
        result = des.shuffle('P', result)
        result = des.xor(result, left_text)
        return right_text, result
