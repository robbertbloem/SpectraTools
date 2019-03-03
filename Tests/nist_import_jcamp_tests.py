"""

"""
import importlib
import unittest
import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import NistTools
import NistTools.Resources.nist_import_jcamp as NIJ

importlib.reload(NIJ)


class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_simple_init(self):
        x = NIJ.NistImportJcamp()
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
            c = NIJ.NistImportJcamp(path = t["path"], filename = t["filename"])
            d = c.import_file()
            self.assertTrue(t["title"] == d["title"])

            





if __name__ == "__main__": 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_import)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)    