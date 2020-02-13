"""

"""
import importlib
import unittest
import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools
import SpectraTools.Resources.spc_import as SPC

importlib.reload(SPC)


class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_simple_init(self):
        x = SPC.SPCImport()
        print(x)
        
class Test_import(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_imports(self):
        tests = [
            {
            "path": pathlib.Path("Testdata/epa"),
            "filename": pathlib.Path("001a4asc.spc"),
            "title": "Acetaldehyde 99.7ppm",
            },
            {
            "path": pathlib.Path("Testdata/epa"),
            "filename": pathlib.Path("104a4ssd.spc"),
            "title": "methanol (SG) 100.0 ppm",
            },
        ]
        
        for t in tests:
            c = SPC.SPCImport(path = t["path"], filename = t["filename"])
            d = c.import_file()
           




if __name__ == "__main__": 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_import)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)    