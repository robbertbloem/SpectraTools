import importlib
import inspect
import os
import warnings
import unittest
import pathlib
import os

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.epa_spectra as EPA

importlib.reload(EPA)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 2
        self.root = pathlib.Path(r"Testdata/epa")


    def test_init(self):
        """
        Basic test: see if the module is loaded.
        
        """
        pass
        
       
class Test_import_data(unittest.TestCase):

    def setUp(self):
        self.verbose = 2
        self.root = pathlib.Path(r"Testdata/epa")
        self.tests = [
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


    def test_import(self):
        
        for t in self.tests:
            e = EPA.epa_spectra(path = t["path"], filename = t["filename"])
            e.import_data(load_all = True)
            
            self.assertTrue(e.spc_record.ofirst == e.x[0])
            self.assertTrue(e.comment == t["title"])

            
    def test_import_loadall_false(self):
        
        for t in self.tests:
            e = EPA.epa_spectra(path = t["path"], filename = t["filename"])
            e.import_data(load_all = False)
            
            self.assertTrue(e.comment == t["title"])
            self.assertTrue(e.x[0] == 4400.76171875)

        
        

if __name__ == '__main__': 
    
    plt.close("all")
    
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)      

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_import_data)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)             
        
          
     