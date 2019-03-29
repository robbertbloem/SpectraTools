"""

"""
import importlib
import unittest
import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

# import NistTools
import NistTools.nist as NIST

importlib.reload(NIST)


class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_simple_init(self):
        x = NIST.nist()
        print(x)
        
class Test_import(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_imports(self):
        tests = [
            {
            "path": pathlib.Path("Testdata/"),
            "filename": pathlib.Path("74-82-8-IR.jdx"),
            "title": "METHANE",
            },
            {
            "path": pathlib.Path("Testdata/"),
            "filename": pathlib.Path("7732-18-5-IR.jdx"),
            "title": "WATER",
            },
            ]
        
        for t in tests:
            c = NIST.nist(path = t["path"], filename = t["filename"])
            d = c.import_data()
            print(c)


    

            





if __name__ == "__main__": 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_import)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)    