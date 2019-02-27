import importlib 
import inspect
import os
import warnings
import unittest

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.LinearSpectrum as LS

importlib.reload(LS)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1



    def test_init(self):
        """
        Basic test
        2019-01-04/RB
        """
        x = numpy.arange(10)
        y = x**2

        x_unit = "cm"
        y_unit = "A"       
        
        P = LS.LinearSpectrum(verbose = self.verbose, x = x, y = y, x_unit = x_unit, y_unit = y_unit)
        
        self.assertTrue(P.x is not None)
        self.assertTrue(P.y is not None)
        
        
    def test_setter_X(self):
        """
        Basic test
        2019-01-07/RB
        """    
        P = LS.LinearSpectrum(verbose = self.verbose)
        test = numpy.arange(10)
        P.x = test
        self.assertTrue(numpy.allclose(P.x, test))


class Test_make_new_x(unittest.TestCase):

    def setUp(self):
        self.verbose = 0
        
    def test_make_bins(self):
        """
        Basic test
        2019-01-04/RB
        """        
        tests = [
            [0.1, numpy.array([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95])],
            [0.11, numpy.array([0.055, 0.165, 0.275, 0.385, 0.495, 0.605, 0.715, 0.825, 0.935])],
        ]
                
        x = numpy.arange(100) / 100
        y = x**2
        
        P = LS.LinearSpectrum(verbose = self.verbose, x = x, y = y)
        
        for t in tests:
            new_x = P.make_new_x(t[0])
            self.assertTrue(numpy.allclose(new_x, t[1]))

        
    def test_make_bins_2(self):
        """
        Basic test
        2019-01-04/RB
        """    
        x = numpy.array([0,1, 2,3, 4,5, 6,7, 8,9], dtype = numpy.float64)
        P = LS.LinearSpectrum(verbose = self.verbose, x = x)
        new_x = P.make_new_x(2.0)

        x = numpy.array([0,1, 2,3, 4,5, 6,7, 8,9])
        P = LS.LinearSpectrum(verbose = self.verbose, x = x)
        new_x = P.make_new_x(2)
                
        
    def test_make_bins_x_not_set(self):
        """
        x was not set. 
        This gives a warning. x will be returned.
        2019-01-04/RB
        """    
        P = LS.LinearSpectrum(verbose = self.verbose)
        x_resolution = 0.1
        new_x = P.make_new_x(x_resolution)
        self.assertTrue(new_x == None) 
        
    def test_bin_data_basic(self):
        """
        Basic test
        2019-01-04/RB
        """    
        x = numpy.array([0,1, 2,3, 4,5, 6,7, 8,9])
        y = numpy.array([1,1, 1,1, 1,2, 2,2, 2,2])
        P = LS.LinearSpectrum(verbose = self.verbose, x = x, y = y)
        new_x = P.make_new_x(2)
        
        new_x, new_y = P.bin_data_helper(new_x)
        
        # print(new_y, [1,1,1.5,2,2])
        
        self.assertTrue(numpy.allclose(new_y[0], [1,1,1.5,2,2]))

    def test_bin_data_bin_boundaries(self):
        """
        Check if binning works. 0 =< x < 2 should be one bin.  
        2019-01-04/RB
        """    
        x = numpy.array([0,0.1,1.9, 2.0,3.9, 4.0,5.9]) 
        y = numpy.array([1,1,1,     2,2,     3,3])
        P = LS.LinearSpectrum(verbose = self.verbose, x = x, y = y)
        new_x = P.make_new_x(2)

        new_x, new_y = P.bin_data_helper(new_x)
        self.assertTrue(numpy.allclose(new_y[0], [1,2,3]))

    def test_bin_data_empty_bin(self):
        """
        There is no data for one bin. This is nan.
        2019-01-04/RB
        """    
        x = numpy.array([0,0.1,1.9, 4.0,5.9, 6.0,7.9]) 
        y = numpy.array([1,1,1,     2,2,     3,3])
        P = LS.LinearSpectrum(verbose = self.verbose, x = x, y = y)
        new_x = P.make_new_x(2)

        new_x, new_y = P.bin_data_helper(new_x)
        self.assertTrue(numpy.isnan(new_y[0,1]))
        new_y = numpy.delete(new_y, 1, axis = 1)
        self.assertTrue(numpy.allclose(new_y[0], [1,2,3]))


    def test_bin_data_use_other_y(self):
        """
        Bin other data than self.y
        2019-01-04/RB
        """    
        x =  numpy.array([0,0.1,1.9, 4.0,5.9, 6.0,7.9]) 
        y1 = numpy.array([4,4,4,     5,5,     6,6])
        y2 = numpy.array([1,1,1,     2,2,     3,3])
        P = LS.LinearSpectrum(verbose = self.verbose, x = x, y = y1)
        new_x = P.make_new_x(2)

        new_x, new_y = P.bin_data_helper(new_x, y = y2)
        self.assertTrue(numpy.isnan(new_y[0,1]))
        new_y = numpy.delete(new_y, 1, axis = 1)
        self.assertTrue(numpy.allclose(new_y, [1,2,3]))        
        
class Test_conversions(unittest.TestCase):

    def setUp(self):
        self.verbose = 0
        
    def test_convert_x(self):
        """
        Basic test
        2019-01-04/RB
        """        
        x = numpy.array([1,1000])        
        P = LS.LinearSpectrum(verbose = self.verbose, x = x)        
        
        tests = [
            ["nm", "nm", [1, 1000], [1, 1000]],
            ["nm", "um", [1, 1000], [0.001, 1]],
            ["nm", "cm-1",  [1, 1000], [1e7, 1e4]],
            ["nm", "ev",  [1, 1000], [1239.84, 1.23984]],

            ["um", "nm",  [1, 1000], [1000, 1e6]],
            ["um", "um",  [1, 1000], [1, 1000]],
            ["um", "cm-1",  [1, 1000], [1e4, 10]],
            ["um", "ev",  [1, 1000], [1.23984, 1.23984/1000]],

            ["cm-1", "nm",  [1, 1000], [1e7, 1e4]],
            ["cm-1", "um",  [1, 1000], [1e4, 10]],
            ["cm-1", "cm-1",  [1, 1000], [1, 1000]],
            ["cm-1", "ev",  [100, 1000], [0.0123984, 0.123984]],
            
            ["ev", "nm",  [1, 1000], [1239.84, 1.23984]],
            ["ev", "um",  [1, 1000], [1.23984, 1.23984/1000]],
            ["ev", "cm-1",  [1, 1000], [8065.54429, 8065544]],  
            ["ev", "ev",  [1, 1000], [1, 1000]],              
        ]
        
        for t in tests:
            P.x = numpy.array(t[2])
            P.x_unit = t[0]
            new_x, x_unit = P.convert_x(t[1])
            s = "{:s} -> {:s}".format(t[0],t[1])
            with self.subTest(s):
                # print(s, new_x, t[3])
                self.assertTrue(numpy.allclose(new_x, t[3]))
        
    def test_convert_x_unknown_new_unit(self):
        """
        Basic test
        2019-01-04/RB
        """        
        x = numpy.array([1,1000])     
        x_unit = "nm"
        P = LS.LinearSpectrum(verbose = self.verbose, x = x, x_unit = x_unit)                
        new_x, x_unit = P.convert_x("bla")
        self.assertTrue(numpy.allclose(new_x, x))

    def test_convert_x_unknown_old_unit(self):
        """
        Basic test
        2019-01-04/RB
        """        
        x = numpy.array([1,1000])     
        x_unit = "bla"
        P = LS.LinearSpectrum(verbose = self.verbose, x = x, x_unit = x_unit)                
        new_x, x_unit = P.convert_x("nm")
        self.assertTrue(numpy.allclose(new_x, x))     

    def test_convert_x_no_x(self):
        """
        Basic test
        2019-01-04/RB
        """        
        x_unit = "nm"
        P = LS.LinearSpectrum(verbose = self.verbose, x_unit = x_unit)                
        new_x, x_unit = P.convert_x("um")

        
        
        
    def test_convert_y(self):
        """
        Basic test
        2019-01-04/RB
        """        
        y = numpy.array([1,1000])        
        P = LS.LinearSpectrum(verbose = self.verbose, y = y)        
        
        tests = [
            ["T1", "T100", [0.5], [50]],
            ["T1", "A", [0.5], [0.30103]],
            
            ["T100", "T1", [50], [0.5]],
            ["T100", "A", [50], [0.30103]],
            
            ["A", "T100", [0.30103], [50]],
            ["A", "T1", [0.30103], [0.5]],
        ]
        
        for t in tests:
            P.y = numpy.array(t[2])
            P.y_unit = t[0]
            new_y, y_unit = P.convert_y(t[1])
            s = "{:s} -> {:s}".format(t[0],t[1])
            with self.subTest(s):
                # print(s, new_y, t[3])
                self.assertTrue(numpy.allclose(new_y, t[3]))
                


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
        P = LS.LinearSpectrum(verbose = self.verbose)
        
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
            P.x = t[0]
            res = P.find_indices_for_cropping(t[1], t[2], pad = 1)
            s = "{:}->{:}, {:}, {:}, {:} ?= {:}".format(t[0][0], t[0][-1], t[1], t[2], t[3], res)
            with self.subTest(s):
                # print(s)
                self.assertTrue(len(res) == len(t[3]))
                self.assertTrue(numpy.allclose(res, t[3]))            

    def test_crop_x_no_xmin_xmax(self):

        P = LS.LinearSpectrum(verbose = self.verbose)
        P.x = numpy.arange(10)
        res = P.find_indices_for_cropping(None, None)
        self.assertTrue(res is None)  
        
    def test_crop_x_xmin_xmax_out_of_range(self):

        P = LS.LinearSpectrum(verbose = self.verbose)
        P.x = numpy.arange(10)
        res = P.find_indices_for_cropping(12, 16)
        self.assertTrue(res is None)          

    def test_crop_x_no_x(self):

        P = LS.LinearSpectrum(verbose = self.verbose)
        res = P.find_indices_for_cropping(2, 8)
        self.assertTrue(res is None)          

    def test_pad_int(self):

        P = LS.LinearSpectrum(verbose = self.verbose)
        P.x = numpy.arange(10)
        res = P.find_indices_for_cropping(min_x = 3.5, max_x = 6.5, pad = 1)
        self.assertTrue(len(res) == 5)
        self.assertTrue(numpy.allclose(res, numpy.arange(3,8)))        

    def test_pad_float(self):

        P = LS.LinearSpectrum(verbose = self.verbose)
        P.x = numpy.arange(25)
        res = P.find_indices_for_cropping(min_x = 8.5, max_x = 13.5, pad = 2.3)
        self.assertTrue(len(res) == 15)
        self.assertTrue(numpy.allclose(res, numpy.arange(4,19)))        








        
if __name__ == '__main__': 
    verbosity = 1
    
    """
    Methods:
    + __init__
    + make_bins
    + get_min_max_x
    

    + crop_x
    + calculate_signal (placeholder)
    + import_data (placeholder)

    + labels_x
    + labels_y
    + plot_spectrum    
    """
    
    if 0:
        """
        + __init__
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)

    if 1:
        """
        + bin_data_helper
        + bin_data
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_make_new_x)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)    
    
    if 0:
        """
        + convert_x
        + convert_y
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_conversions)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)      
    
    if 0:
        """
        + find_indices_for_cropping
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_find_indices_for_cropping)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)       
        
    # if 1:
        # """
        # + calculate_transmission_for_pathlength
        # """
        # suite = unittest.TestLoader().loadTestsFromTestCase(Test_calculate_transmission_for_pathlength)
        # unittest.TextTestRunner(verbosity=verbosity).run(suite)             