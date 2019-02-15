import importlib 
import inspect
import os
import warnings
import unittest

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import RefractiveIndexTools.RefractiveIndex as RI

importlib.reload(RI)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1



    def test_init(self):
        """
        Basic test
        2019-02-05/RB
        """
        c = RI.RefractiveIndex()
        
 








        
if __name__ == '__main__': 
    verbosity = 1

    
    if 1:
        """
        + __init__
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)

           