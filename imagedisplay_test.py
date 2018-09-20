import imagedisplay
import unittest
import numpy as np

'''
Unit tests for imagedisplay.py
'''

'''
More tests to write:
init:
calibration is a string
input is 1d
input is non-number



'''

class ImageDisplayTest(unittest.TestCase):

    def testInit3DIm(self):
        '''an error is raised given a 3d input'''
        im = np.arange(8).reshape(2, 2, 2)
        with self.assertRaisesRegex(ValueError, 
            'Your image is not 2D! Please check the number of dimensions '
            'in the input!'):
            disp = imagedisplay.ImageDisplay(im, cal=None)
            
if __name__ == '__main__':
    unittest.main()      
