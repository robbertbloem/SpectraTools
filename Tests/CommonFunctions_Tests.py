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
        

    def test_basic_old(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(5, 100)
        x2 = numpy.linspace(50, 150)
        
        start, finish = CF.find_overlap_in_arrays(x1 = x1, x2 = x2)
        self.assertTrue(numpy.allclose(start, 50))
        self.assertTrue(numpy.allclose(finish, 100))
        # self.assertTrue(finish == 100)        

    def test_basic(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(5, 100)
        x2 = numpy.linspace(50, 150)
        
        start, finish = CF.find_overlap_in_arrays(x_list = [x1, x2])
        self.assertTrue(numpy.allclose(start, 50))
        self.assertTrue(numpy.allclose(finish, 100))    

        
    def test_negative_numbers_old(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(-5, -100)
        x2 = numpy.linspace(-50, -150)
        
        start, finish = CF.find_overlap_in_arrays(x1 = x1, x2 = x2) 
        self.assertTrue(numpy.allclose(start, -100))
        self.assertTrue(numpy.allclose(finish, -50))            
        
        
    def test_negative_numbers(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(-5, -100)
        x2 = numpy.linspace(-50, -150)
        
        start, finish = CF.find_overlap_in_arrays(x_list = [x1, x2])
        self.assertTrue(numpy.allclose(start, -100))
        self.assertTrue(numpy.allclose(finish, -50))    

    def test_nan_old(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(-5, -100)
        x2 = numpy.linspace(-50, -150)
        x1[10] = numpy.nan
        
        start, finish = CF.find_overlap_in_arrays(x1 = x1, x2 = x2)

        self.assertTrue(numpy.allclose(start, -100))
        self.assertTrue(numpy.allclose(finish, -50))     

    def test_nan(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = numpy.linspace(-5, -100)
        x2 = numpy.linspace(-50, -150)
        x1[10] = numpy.nan
        
        start, finish = CF.find_overlap_in_arrays(x_list = [x1, x2])

        self.assertTrue(numpy.allclose(start, -100))
        self.assertTrue(numpy.allclose(finish, -50))            
        
    def test_input_is_range_old(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = range(5, 101)
        x2 = range(50, 150)

        start, finish = CF.find_overlap_in_arrays(x1 = x1, x2 = x2)

        self.assertTrue(numpy.allclose(start, 50))
        self.assertTrue(numpy.allclose(finish, 100))             

    def test_input_is_range(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = range(5, 101)
        x2 = range(50, 150)

        start, finish = CF.find_overlap_in_arrays(x_list = [x1, x2])

        self.assertTrue(numpy.allclose(start, 50))
        self.assertTrue(numpy.allclose(finish, 100))             
        
    def test_input_is_list_old(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = [1,2,3,4,5,6,7,8,9,10]
        x2 = [5,6,7,8,9,10,11,12,13]

        start, finish = CF.find_overlap_in_arrays(x1 = x1, x2 = x2)

        self.assertTrue(numpy.allclose(start, 5))
        self.assertTrue(numpy.allclose(finish, 10))     

    def test_input_is_list(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = [1,2,3,4,5,6,7,8,9,10]
        x2 = [5,6,7,8,9,10,11,12,13]

        start, finish = CF.find_overlap_in_arrays(x_list = [x1, x2])

        self.assertTrue(numpy.allclose(start, 5))
        self.assertTrue(numpy.allclose(finish, 10))            
        
        
    def test_input_is_int_x1_old(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = None
        x2 = [1,2,3,4,5,6,7,8,9,10]

        start, finish = CF.find_overlap_in_arrays(x1 = x1, x2 = x2)

        self.assertTrue(start is None)
        self.assertTrue(finish is None)            

    def test_input_is_int_x1(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = None
        x2 = [1,2,3,4,5,6,7,8,9,10]

        start, finish = CF.find_overlap_in_arrays(x_list = [x1, x2])

        self.assertTrue(start is None)
        self.assertTrue(finish is None)            


    def test_input_is_int_x2_old(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = [1,2,3,4,5,6,7,8,9,10]
        x2 = None

        start, finish = CF.find_overlap_in_arrays(x1 = x1, x2 = x2)

        self.assertTrue(start is None)
        self.assertTrue(finish is None)             
        

    def test_input_is_int_x2(self):
        """
        Basic test.
        2019-01-11/RB
        """
        x1 = [1,2,3,4,5,6,7,8,9,10]
        x2 = None

        start, finish = CF.find_overlap_in_arrays(x_list = [x1, x2])

        self.assertTrue(start is None)
        self.assertTrue(finish is None)     
        
    def test_cases_old(self):
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
            start, finish = CF.find_overlap_in_arrays(x1 = t[1], x2 = t[2])

            if t[3] is None:
                s = "{:s}: start: {:} ?= None, finish: {:} ?= None".format(t[0], start, finish)
                with self.subTest(s):            
                    self.assertTrue(start is None)
                    self.assertTrue(finish is None)
            else:
                s = "{:s}: start: {:} ?= {:}, finish: {:} ?= {:}".format(t[0], start, t[3][0], finish, t[3][1])
                with self.subTest(s):   
                    self.assertTrue(numpy.allclose(start, t[3][0]))
                    self.assertTrue(numpy.allclose(finish, t[3][1]))
      


        
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
            start, finish = CF.find_overlap_in_arrays(x_list = [t[1], t[2]])

            if t[3] is None:
                s = "{:s}: start: {:} ?= None, finish: {:} ?= None".format(t[0], start, finish)
                with self.subTest(s):            
                    self.assertTrue(start is None)
                    self.assertTrue(finish is None)
            else:
                s = "{:s}: start: {:} ?= {:}, finish: {:} ?= {:}".format(t[0], start, t[3][0], finish, t[3][1])
                with self.subTest(s):                
                    self.assertTrue(numpy.allclose(start, t[3][0]))
                    self.assertTrue(numpy.allclose(finish, t[3][1]))          

class Test_indices_for_binning(unittest.TestCase):

    def setUp(self):
        self.verbose = 0
        
        
    def test_basic(self):
        tests = [
            {
            "s": "simple",
            "x":   numpy.array([0,1, 2,3, 4,5, 6,7, 8,9]),
            "test":  numpy.array([0,0, 1,1, 2,2, 3,3, 4,4]),
            "new_x": numpy.array([1, 3, 5, 7, 9]),
            },{
            "s": "missing in x", 
            "x":   numpy.array([2,3,4,1,6,8]),
            "test":  numpy.array([1,1,2,0,3,4]),
            "new_x": numpy.array([1, 3, 5, 7, 9]),
            },{
            "s": "x over value", 
            "x":   numpy.array([-2,-1,   0,1,2,3,4,5,6,7,8,9, 10,11]),
            "test":  numpy.array([-1,-1, 0,0,1,1,2,2,3,3,4,4, -1,-1]),
            "new_x": numpy.array([1, 3, 5, 7, 9]),
            },
        ]
        
        for t in tests:
            with self.subTest(t["s"]):
                res = CF.indices_for_binning(t["x"], t["new_x"])
                print("res", res)
                self.assertTrue(numpy.allclose(res, t["test"]))

class Test_get_min_max_x(unittest.TestCase):

    def setUp(self):
        self.verbose = 0
        
        
    def test_1(self):
        
        x = numpy.arange(10)
        min_x, max_x = CF.get_min_max_x(x = x)
        self.assertTrue(min_x == 0)
        self.assertTrue(max_x == 9)
        
    def test_min_x_given(self):
        
        x = numpy.arange(10)
        min_x, max_x = CF.get_min_max_x(x = x, min_x = -3)
        self.assertTrue(min_x == -3)
        self.assertTrue(max_x == 9)        

    def test_max_x_given(self):
        
        x = numpy.arange(10)
        min_x, max_x = CF.get_min_max_x(x = x, max_x = 12)
        self.assertTrue(min_x == 0)
        self.assertTrue(max_x == 12)          
        
    def test_x_list(self):
        
        x = range(10)
        min_x, max_x = CF.get_min_max_x(x = x)
        self.assertTrue(min_x == 0)
        self.assertTrue(max_x == 9)      

    def test_x_int(self):
        
        x = 10
        min_x, max_x = CF.get_min_max_x(x = x)
        self.assertTrue(min_x == 10)
        self.assertTrue(max_x == 10)   

    @unittest.expectedFailure
    def test_x_str(self):
        
        x = "a"
        min_x, max_x = CF.get_min_max_x(x = x)

        
class Test_find_indices_for_cropping(unittest.TestCase):

    def setUp(self):
        self.verbose = 0
        
    def test_crop_x(self):
        """
        Basic test
        2019-01-08/RB
        
        x1
        idx 0 1 2 3 4 5 6 7 8 9
        val 0 1 2 3 4 5 6 7 8 9

        x2
        idx 0 1 2 3 4 5 6 7 8 9
        val 9 8 7 6 5 4 3 2 1 0

        x3
        idx 0  1  2  3  4  5  6  7  8  9
        val 0 -1 -2 -3 -4 -5 -6 -7 -8 -9
        
        x4
        idx  0  1  2  3  4  5  6  7  8  9
        val -9 -8 -7 -6 -5 -4 -3 -2 -1  0        
        
        """        
        
        
        x1 = numpy.arange(10)
        x2 = numpy.arange(10)[::-1]
        x3 = -numpy.arange(10)
        x4 = -numpy.arange(10)[::-1]        
        
        tests = [
            [x1, 3.5, 6.5, numpy.arange(3,8)],
            [x1, 3, 6, numpy.arange(2,8)],
            [x1, -1, 6.5, numpy.arange(8)],
            [x1, 3.5, 11, numpy.arange(3,10)],
            [x1, -1, 11, numpy.arange(10)],            
            
            [x2, 3.5, 6.5, numpy.array([2,3,4,5,6])],
            [x2, 3, 6, numpy.arange(2,8)],
            [x2, -1, 6.5, numpy.arange(2,10)],
            [x2, 2.5, 11, numpy.arange(8)],    
            [x2, -1, 11, numpy.arange(10)],               

            [x3, -3.5, -6.5, numpy.arange(3,8)],
            [x3, -3, -6, numpy.arange(2,8)],
            [x3, 1, -6.5, numpy.arange(8)],
            [x3, -3.5, -11, numpy.arange(3,10)],
            [x3, -1, -11, numpy.arange(10)],   
            
            [x4, -3.5, -6.5, numpy.array([2,3,4,5,6])],
            [x4, -3, -6, numpy.arange(2,8)],
            [x4, 1, -6.5, numpy.arange(2,10)],
            [x4, -3.5, -11, numpy.arange(7)],    
            [x4, -1, -11, numpy.arange(10)],   
            
            [x1, None, 6.5, numpy.arange(8)],
            [x1, 3.5, None, numpy.arange(3,10)],
          
        ]
       
        for t in tests:
            res = CF.find_indices_for_cropping(x = t[0], min_x = t[1], max_x = t[2], pad = 1, verbose = self.verbose)
            s = "{:}->{:}, {:}, {:}, {:} ?= {:}".format(t[0][0], t[0][-1], t[1], t[2], t[3], res)
            with self.subTest(s):
                # print(s)
                self.assertTrue(len(res) == len(t[3]))
                self.assertTrue(numpy.allclose(res, t[3]))            

    def test_crop_x_no_xmin_xmax(self):

        x = numpy.arange(10)
        res = CF.find_indices_for_cropping(x, None, None, verbose = self.verbose)
        self.assertTrue(res is None)  
        
    def test_crop_x_xmin_xmax_out_of_range(self):

        x = numpy.arange(10)
        res = CF.find_indices_for_cropping(x, 12, 16, verbose = self.verbose)
        self.assertTrue(res is None)                 

    def test_pad_int(self):

        x = numpy.arange(10)
        res = CF.find_indices_for_cropping(x = x, min_x = 3.5, max_x = 6.5, pad = 1, verbose = self.verbose)
        self.assertTrue(len(res) == 5)
        self.assertTrue(numpy.allclose(res, numpy.arange(3,8)))        

    def test_pad_float(self):

        x = numpy.arange(25)
        res = CF.find_indices_for_cropping(x = x, min_x = 8.5, max_x = 13.5, pad = 2.3, verbose = self.verbose)
        self.assertTrue(len(res) == 15)
        self.assertTrue(numpy.allclose(res, numpy.arange(4,19)))             
        
        

if __name__ == '__main__': 

    verbosity = 1
        
    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)      
    
    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_find_overlap_in_arrays)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)             

    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_indices_for_binning)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)              

    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_get_min_max_x)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)     

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_find_indices_for_cropping)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)          