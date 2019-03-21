from importlib import reload
import inspect
import os
import warnings
import unittest
import pathlib
import os

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.hitran as HR

reload(HR)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 2



    def test_init(self):
        """
        Basic test: see if the module is loaded.
        2019-03-20/RB
        """
        pass
        
       
    def test_setup_db(self):
        """
        2019-03-20/RB
        """
        db_path = pathlib.Path(r"Testdata/hitran_data")
        
                
        tablename = "H2O"
        M = 1
        I = 1
        min_x = 1200
        max_x = 1300
        
        c = HR.hitran(db_path, tablename, M, I, min_x, max_x, verbose = self.verbose)
        
    def test_fetch_data(self):
        """
        
        
        """
        db_path = pathlib.Path(r"Testdata/hitran_data")
        
        tablename = "H2O"
        M = 1
        I = 1
        min_x = 1200
        max_x = 1300
        
        c = HR.hitran(db_path, tablename, M, I, min_x, max_x, verbose = self.verbose)
        
        c.import_data()
        

    def test_fetch_data_2(self):
        """
        
        
        """
        db_path = pathlib.Path(r"Testdata/hitran_data")
        
        tablename = "a"
        M = 1
        I = 1
        min_x = 1200
        max_x = 1300
        
        c = HR.hitran(db_path, tablename, M, I, min_x, max_x, verbose = self.verbose)
        
        c.import_data()
        
        c.remove_data()
        

        
class Test_calculate_signal(unittest.TestCase):

    def setUp(self):
        self.verbose = 1


    def test_fetch_data(self):
        """
        
        
        """
        db_path = pathlib.Path(r"Testdata/hitran_data")
        
        tablename = "H2O"
        M = 1
        I = 1
        min_x = 1200
        max_x = 1300
        
        c = HR.hitran(db_path, tablename, M, I, min_x, max_x, verbose = self.verbose)
        
        c.import_data()

        c.calculate_signal()
        
        print(c.x)
        print(c.y)
        
        

if __name__ == '__main__': 

    verbosity = 1
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)      

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_calculate_signal)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)          
     