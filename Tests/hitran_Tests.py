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

import SpectraTools.hitran as HR

importlib.reload(HR)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 2
        self.root = pathlib.Path(r"Testdata/hitran_data")


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
        db_path = self.root
        
                
        tablename = "H2O"
        M = 1
        I = 1
        min_x = 1200
        max_x = 1300
        
        c = HR.hitran(db_path, tablename, M, I, min_x, max_x, verbose = self.verbose)

class Test_import_data(unittest.TestCase):

    def setUp(self):
        self.verbose = 2
        self.root = pathlib.Path(r"Testdata/hitran_data")
        
    def is_file_present(self, tablename, extension, should_be_present):
        """
        Check if a file is present or not
        
        Keyword Arguments
        -----------------
        tablename : str
            Name of the table
        extenstion : str
            Usually 'data' or 'header'
        should_be_present : bool
            If True, the test will be a success if the file is present. If False, the test is successful if the file is absent. 
        
        Notes
        -----
        
        2019-03-21/RB
        """
    
        filename = pathlib.Path("{:s}.{:s}".format(tablename, extension))
        paf = self.root.joinpath(filename)
        
        test = paf.is_file()
        
        if should_be_present:
            self.assertTrue(test)
        else:
            self.assertFalse(test)
            
        return test

    def test_absence_of_file_1(self):
        """
        
        2019-03-21/RB
        """
        tablename = "fiets"
        extension = "auto"
        should_be_present = False
        self.is_file_present(tablename, extension, should_be_present)
        
    
    @unittest.expectedFailure
    def test_absence_of_file_2(self):
        """
        
        2019-03-21/RB
        """
        tablename = "fiets"
        extension = "auto"
        should_be_present = True
        self.is_file_present(tablename, extension, should_be_present)
        
    def test_fetch_data_already_present(self):
        """
        
        2019-03-21/RB
        """
        db_path = self.root
        
        tablename = "H2O - test_fetch_data_already_present"
        M = 1
        I = 1
        min_x = 1240
        max_x = 1280
        
        c = HR.hitran(db_path, tablename, M, I, min_x, max_x, verbose = self.verbose)
        
        test1 = self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        test2 = self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)        
        
        if not test1 or not test2:
            print("hitran_Tests.Test_import_data.test_fetch_data_already_present(): files should have been present before importing, but they aren't. Please run the test again.  ")
        
        c.import_data(reload = False)
        
        self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)        
        

    def test_fetch_data_new_data(self):
        """
        
        2019-03-20/RB
        """
        db_path = self.root
        
        tablename = "H2O - test_fetch_data_new_data"
        M = 1
        I = 1
        min_x = 1240
        max_x = 1280
        
        c = HR.hitran(db_path, tablename, M, I, min_x, max_x, verbose = self.verbose)
        
        c.import_data()

        self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)

        c.remove_data(remove_without_confirmation = True)

        self.is_file_present(tablename = tablename, extension = "header", should_be_present = False)
        self.is_file_present(tablename = tablename, extension = "data", should_be_present = False)


      
        
    def test_fetch_data_reload(self):
        """
        
        2019-03-20/RB
        """
        db_path = pathlib.Path(self.root)
        
        tablename = "H2O - test_fetch_data_reload"
        M = 1
        I = 1
        min_x = 1240
        max_x = 1280
        
        c = HR.hitran(db_path, tablename, M, I, min_x, max_x, verbose = self.verbose)
        
        test1 = self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        test2 = self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)        
        
        if not test1 or not test2:
            print("hitran_Tests.Test_import_data.test_fetch_data_reload(): files should have been present before importing, but they aren't. Please run the test again.  ")
        
        c.import_data(reload = True)
        
        self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)   


        
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
        min_x = 1240
        max_x = 1280
        
        c = HR.hitran(db_path, tablename, M, I, min_x, max_x, verbose = self.verbose)
        
        c.import_data()

        c.calculate_signal()
        
        self.assertTrue(numpy.isclose(c.x[0], 1240.362354))
        self.assertTrue(numpy.isclose(c.x[-1], 1279.932354))
        self.assertTrue(numpy.isclose(c.y[0], 0.00276249))
        self.assertTrue(numpy.isclose(c.y[-1], 0.00111738))
        
        self.assertTrue(c.y_unit == "A")
        
        
        
        

if __name__ == '__main__': 

    verbosity = 1
        
    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)      

    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_import_data)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)             
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_calculate_signal)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)          
     