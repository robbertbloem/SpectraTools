from importlib import reload
import inspect
import os
import warnings
import unittest

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.Resources.CommonFunctions as CF

reload(CF)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 0



    def test_init(self):
        """
        Basic test: see if the module is loaded.
        2019-01-11/RB
        """
        pass
        
       


class Test_find_overlap_in_arrays(unittest.TestCase):

    def setUp(self):
        self.verbose = 0

    def test_basic(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(5, 100)
        x2 = numpy.linspace(50, 150)
        
        start, finish = CF.find_overlap_in_arrays(x1, x2)
        self.assertTrue(start == 50)
        self.assertTrue(finish == 100)        

        
    def test_negative_numbers(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(-5, -100)
        x2 = numpy.linspace(-50, -150)
        
        start, finish = CF.find_overlap_in_arrays(x1, x2)
        self.assertTrue(start == -100)
        self.assertTrue(finish == -50)    

    def test_nan(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(-5, -100)
        x2 = numpy.linspace(-50, -150)
        x1[10] = numpy.nan
        
        start, finish = CF.find_overlap_in_arrays(x1, x2)

        self.assertTrue(start == -100)
        self.assertTrue(finish == -50)    

    def test_input_is_range(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = range(5, 101)
        x2 = range(50, 150)

        start, finish = CF.find_overlap_in_arrays(x1, x2)

        self.assertTrue(start == 50)
        self.assertTrue(finish == 100)            

    def test_input_is_list(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = [1,2,3,4,5,6,7,8,9,10]
        x2 = [5,6,7,8,9,10,11,12,13]

        start, finish = CF.find_overlap_in_arrays(x1, x2)

        self.assertTrue(start == 5)
        self.assertTrue(finish == 10)    

        
    def test_input_is_int_x1(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = None
        x2 = [1,2,3,4,5,6,7,8,9,10]

        start, finish = CF.find_overlap_in_arrays(x1, x2)

        self.assertTrue(start is None)
        self.assertTrue(finish is None)            


    def test_input_is_int_x2(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = [1,2,3,4,5,6,7,8,9,10]
        x2 = None

        start, finish = CF.find_overlap_in_arrays(x1, x2)

        self.assertTrue(start is None)
        self.assertTrue(finish is None)     
        
        
    def test_cases(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(30, 60)
        
        tests = [
            ["a", x1, numpy.linspace(0, 10), None],
            ["b", x1, numpy.linspace(20, 40), [30.0, 40.0]],
            ["c", x1, numpy.linspace(40, 50), [40.0, 50.0]],
            ["d", x1, numpy.linspace(50, 70), [50.0, 60.0]],
            ["e", x1, numpy.linspace(70, 80), None],
            ["f", x1, numpy.linspace(20, 70), [30.0, 60.0]],

            ["a -", -x1, -numpy.linspace(70, 80), None],
            ["b -", -x1, -numpy.linspace(50, 70), [-60.0, -50.0]],
            ["c -", -x1, -numpy.linspace(40, 50), [-50.0, -40.0]],
            ["d -", -x1, -numpy.linspace(20, 40), [-40.0, -30.0]],
            ["e -", -x1, -numpy.linspace(0, 10), None],
            ["f -", -x1, -numpy.linspace(20, 70), [-60.0, -30.0]],            
        ]
        
        for t in tests:        
            start, finish = CF.find_overlap_in_arrays(t[1], t[2])

            if t[3] is None:
                s = "{:s}: start: {:} ?= None, finish: {:} ?= None".format(t[0], start, finish)
                with self.subTest(s):            
                    self.assertTrue(start is None)
                    self.assertTrue(finish is None)
            else:
                s = "{:s}: start: {:} ?= {:}, finish: {:} ?= {:}".format(t[0], start, t[3][0], finish, t[3][1])
                with self.subTest(s):                
                    self.assertEqual(start, t[3][0])
                    self.assertEqual(finish, t[3][1])                



       

if __name__ == '__main__': 

    verbosity = 1
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)      
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_find_overlap_in_arrays)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)             

        



     