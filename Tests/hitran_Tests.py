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
import NistTools.nist as NIST

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
        
        c = HR.hitran(db_path, tablename, [(M,I)], min_x, max_x, verbose = self.verbose)

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
        
        c = HR.hitran(db_path, tablename, [(M,I)], min_x, max_x, verbose = self.verbose)
        
        test1 = self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        test2 = self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)        
        
        if not test1 or not test2:
            print("hitran_Tests.Test_import_data.test_fetch_data_already_present(): files should have been present before importing, but they aren't. Please run the test again.  ")
        
        c.import_data(reload = False)
        
        self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)        
        
        # c.remove_data(remove_without_confirmation = True)
        

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
        
        c = HR.hitran(db_path, tablename, [(M,I)], min_x, max_x, verbose = self.verbose)
        
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
        
        c = HR.hitran(db_path, tablename, [(M,I)], min_x, max_x, verbose = self.verbose)
        
        test1 = self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        test2 = self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)        
        
        if not test1 or not test2:
            print("hitran_Tests.Test_import_data.test_fetch_data_reload(): files should have been present before importing, but they aren't. Please run the test again.  ")
        
        c.import_data(reload = True)
        
        self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)   

        # c.remove_data(remove_without_confirmation = True)

        
    def test_fetch_multiple_data(self):
        """
        
        2019-03-20/RB
        """
        db_path = pathlib.Path(self.root)
        
        tablename = "test_fetch_multiple_data"
        components = [(1,1), (6,1)]
        min_x = 1240
        max_x = 1280
        
        c = HR.hitran(db_path, tablename, components, min_x, max_x, verbose = self.verbose)
        
        test1 = self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        test2 = self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)        
        
        if not test1 or not test2:
            print("hitran_Tests.Test_import_data.test_fetch_data_reload(): files should have been present before importing, but they aren't. Please run the test again.  ")
        
        c.import_data()
        
        self.is_file_present(tablename = tablename, extension = "header", should_be_present = True)
        self.is_file_present(tablename = tablename, extension = "data", should_be_present = True)   

        # c.remove_data(remove_without_confirmation = True)        
        
        
        
class Test_calculate_signal(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        self.root = pathlib.Path(r"Testdata/hitran_data")


    def test_calculate_signal(self):
        """
        
        
        """
        db_path = self.root
        
        tablename = "H2O"
        M = 1
        I = 1
        min_x = 1240
        max_x = 1280
        
        c = HR.hitran(db_path, tablename, [(M,I)], min_x, max_x, y_unit = "A", verbose = self.verbose)
        
        c.import_data()

        c.calculate_signal()

        # print(c.x)
        # print(c.y)
        
        self.assertTrue(numpy.isclose(c.x[0], 1240.362354))
        self.assertTrue(numpy.isclose(c.x[-1], 1279.932354))
        self.assertTrue(numpy.isclose(c.y[0], 2.7663e-05))
        self.assertTrue(numpy.isclose(c.y[-1], 1.1180e-05))
        
        self.assertTrue(c.y_unit == "A")
    
    @unittest.expectedFailure
    def test_calculate_signal_wrong_y_unit(self):
        """
        
        
        """
        db_path = self.root
        
        tablename = "H2O"
        M = 1
        I = 1
        min_x = 1240
        max_x = 1280
        
        c = HR.hitran(db_path, tablename, [(M, I)], min_x, max_x, verbose = self.verbose, y_unit = "fiets")
        
        c.import_data()

        c.calculate_signal()        
        
    @unittest.expectedFailure
    def test_calculate_signal_wrong_line_profile(self):
        """
        
        
        """
        db_path = self.root
        
        tablename = "H2O"
        M = 1
        I = 1
        min_x = 1240
        max_x = 1280
        
        c = HR.hitran(db_path, tablename, [(M, I)], min_x, max_x, verbose = self.verbose)
        
        c.import_data()

        c.calculate_signal(line_profile = "fiets")     

   
    def test_signal_multiple_data(self):
        """
        
        2019-03-20/RB
        """
        db_path = pathlib.Path(self.root)
        
        tablename = "test_signal_multiple_data"
        components = [(1,1), (6,1)]
        min_x = 1240
        max_x = 1280
        
        c = HR.hitran(db_path, tablename, components, min_x, max_x, verbose = self.verbose)
        
        c.import_data()
        
        c.calculate_signal()

        # print(c.x)
        # print(c.y)  

        self.assertTrue(numpy.isclose(c.x[0], 1240.018764))
        self.assertTrue(numpy.isclose(c.x[-1], 1279.978764))
        self.assertTrue(numpy.isclose(c.y[0], 0.97829301))
        self.assertTrue(numpy.isclose(c.y[-1], 0.98364074))
        
        self.assertTrue(c.y_unit == "T1")
        
        
        
        

    def test_signal_multiple_data_separate(self):
        """
        
        2019-03-20/RB
        """
        db_path = pathlib.Path(self.root)

        min_x = 1240
        max_x = 1280
        
        tablename = "test_signal_multiple_data_separate_A"
        components_A = [(1,1)]
        a = HR.hitran(db_path, tablename, components_A, min_x, max_x, verbose = self.verbose)
        a.import_data()
        a.calculate_signal()
        
        tablename = "test_signal_multiple_data_separate_B"
        components_B = [(6,1)]
        b = HR.hitran(db_path, tablename, components_B, min_x, max_x, verbose = self.verbose)
        b.import_data()
        b.calculate_signal()
        
        tablename = "test_signal_multiple_data_separate_AB"
        components_AB = [(6,1),(1,1)]
        ab = HR.hitran(db_path, tablename, components_AB, min_x, max_x, verbose = self.verbose)        
        ab.import_data(reload = True)
        ab.calculate_signal()

         
        plt.plot(a.x, a.y, label = "A")
        plt.plot(b.x, b.y, label = "B")
        plt.plot(ab.x, ab.y, label = "AB")
        plt.legend()
        plt.show()        
        
        
        
class Test_data_confirmation(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        self.root = pathlib.Path(r"Testdata/hitran_data")

    def test_calculate_signal(self):
        """
        
        
        """
        db_path = self.root
        
        tablename = "methane"
        M = 6
        I = 1
        min_x = 1160
        max_x = 1420
        
        c = HR.hitran(db_path, tablename, [(M, I)], min_x, max_x, verbose = self.verbose, y_unit = "T1")      
        c.import_data()
        
        p = 150 # mm Hg
        p *= 133.3224 # Pa
        p /= 1e5 # 100 kPa

        environment = {"l": 5, "p": p}
        c.calculate_signal(OmegaStep = 2)

        
        nist_path = self.root
        nist_filename = "74-82-8-IR.jdx"
        n = NIST.nist(path = self.root, filename = nist_filename)
        n.import_data()
        
        n.crop_x(min_x = min_x, max_x = max_x)
        
        
        plt.plot(c.x, c.y, label = "HITRAN")
        plt.plot(n.x, n.y, label = "NIST")
        plt.legend()
        plt.show()
        
        

if __name__ == '__main__': 
    
    plt.close("all")
    
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

    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_data_confirmation)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)             
     