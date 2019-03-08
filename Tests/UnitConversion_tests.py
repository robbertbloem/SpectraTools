import importlib 
import inspect
import os
import warnings
import unittest

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.UnitConversion as UC

importlib.reload(UC)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1



    def test_init(self):
        """
        Just checking if it loads.
        """
        pass
    


class Test_base10_conversion(unittest.TestCase):

    def setUp(self):
        self.verbose = 1



    def test_prefixes(self):
        """
        Just checking if it loads.
        """
        tests = [
        {
            "value": 1,
            "old_base": "micro",
            "new_base": "milli",
            "power": 1,
            "answer": 1e-3,       
        }, {
            "value": 1,
            "old_base": "milli",
            "new_base": "micro",
            "power": 1,
            "answer": 1e3,       
        }, {
            "value": 1,
            "old_base": 0,
            "new_base": "deci",
            "power": 1,
            "answer": 10,       
        }, {
            "value": 1,
            "old_base": 0,
            "new_base": "deci",
            "power": 2,
            "answer": 100,       
        }, {
            "value": 1,
            "old_base": 0,
            "new_base": "deci",
            "power": 3,
            "answer": 1000,       
        }, 
        ]
        
        for t in tests:
            res = UC.base10_to_base10(t["value"], old_base = t["old_base"], new_base = t["new_base"], power = t["power"])
            self.assertTrue(numpy.allclose(res, t["answer"]))



class Test_conversions(unittest.TestCase):
    """
    convert_x and convert_y started as functions in LinearSpectrum. These tests were originally written for this situation. On 2019-03-04 the function was copied (not yet moved) to UnitConversions. These tests were copied as well. 
    
    """

    def setUp(self):
        self.verbose = 0
        
    def test_convert_x(self):
        """
        Basic test
        2019-01-04/RB: started
        2019-03-04/RB: adapted for UnitConversion
        """        
        x = numpy.array([1,1000])        
        
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
            x = numpy.array(t[2])
            new_x, x_unit = UC.convert_x(x = x, old_unit = t[0], new_unit = t[1])
            s = "{:s} -> {:s}".format(t[0],t[1])
            with self.subTest(s):
                # print(s, new_x, t[3])
                self.assertTrue(numpy.allclose(new_x, t[3]))
        
    def test_convert_x_unknown_new_unit(self):
        """
        Basic test
        2019-01-04/RB
        2019-03-04/RB: adapted for UnitConversion
        """        
        x = numpy.array([1,1000])     
        new_x, x_unit = UC.convert_x(x = x, old_unit = "nm", new_unit = "bla")
        self.assertTrue(new_x is None)
        self.assertTrue(x_unit is None)

    def test_convert_x_unknown_old_unit(self):
        """
        Basic test
        2019-01-04/RB
        2019-03-04/RB: adapted for UnitConversion
        """        
        x = numpy.array([1,1000])     
        new_x, x_unit = UC.convert_x(x = x, old_unit = "bla", new_unit = "nm")
        self.assertTrue(new_x is None)
        self.assertTrue(x_unit is None) 


        
        
        
    def test_convert_y(self):
        """
        Basic test
        2019-01-04/RB
        """        
  
        tests = [
            ["T1", "T100", [0.5], [50]],
            ["T1", "A", [0.5], [0.30103]],
            
            ["T100", "T1", [50], [0.5]],
            ["T100", "A", [50], [0.30103]],
            
            ["A", "T100", [0.30103], [50]],
            ["A", "T1", [0.30103], [0.5]],
        ]
        
        for t in tests:
            y = numpy.array(t[2])
            new_y, y_unit = UC.convert_y(y = y, old_unit = t[0], new_unit = t[1])
            
            s = "{:s} -> {:s}".format(t[0],t[1])
            with self.subTest(s):
                # print(s, new_y, t[3])
                self.assertTrue(numpy.allclose(new_y, t[3]))
                
class Test_advanced_conversion(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
    def test_transmission_to_transmission(self):
        tests = [
        {   
            "name": "T1: 0.1 -> 1.0, no change",
            "T": numpy.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]),
            "c": 1,
            "l": 1, 
            "c_new": 1,
            "l_new": 1,
            "T_unit": "T1",
            "answer": numpy.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]),
        }, {   
            "name": "T1: 0.1 -> 1.0, double concentration",
            "T": numpy.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]),
            "c": 1,
            "l": 1, 
            "c_new": 2,
            "l_new": 1,
            "T_unit": "T1",
            "answer": numpy.array([0.01, 0.04, 0.09, 0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1]),
        }, {   
            "name": "T1: 0.1 -> 1.0, double path length ",
            "T": numpy.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]),
            "c": 1,
            "l": 1, 
            "c_new": 1,
            "l_new": 2,
            "T_unit": "T1",
            "answer": numpy.array([0.01, 0.04, 0.09, 0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1]),
        }, {
            "name": "T1 includes 0",
            "T": numpy.array([0, 0.5, 1]),
            "c": 1,
            "l": 1, 
            "c_new": 2,
            "l_new": 1,
            "T_unit": "T1",
            "answer": numpy.array([numpy.nan, 0.25, 1]),
        }
        ]
     
        for t in tests:
            s = "{:s}".format(t["name"])
            with self.subTest(s):           
                res = UC.transmission_to_transmission(T = t["T"], c = t["c"], l = t["l"], c_new = t["c_new"], l_new = t["l_new"], T_unit = t["T_unit"])
                answer = t["answer"]
                idx_res = numpy.asarray(numpy.isfinite(res)).nonzero()[0]
                idx_answer = numpy.asarray(numpy.isfinite(answer)).nonzero()[0]
                self.assertTrue(numpy.all(idx_res == idx_answer))
                res = res[idx_res]
                answer = answer[idx_answer]
                # print(res, answer)
                self.assertTrue(numpy.allclose(res, answer))
            
            


if __name__ == '__main__': 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_base10_conversion)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)
        
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_conversions)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)  
        
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_advanced_conversion)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)                