import importlib 
import inspect
import os
import warnings
import unittest

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.PressureCalculations as PC

importlib.reload(PC)

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1



    def test_init(self):
        """
        Just checking if it loads.
        """
        pass
    

class Test_calculations(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def test_water_vapour_saturation_pressure(self):
        
        tests = [
            {"Tin": 293.15, "isCelsius": False, "Pout": 2339.19},
            {"Tin": 20, "isCelsius": True, "Pout": 2339.19},
            # {"Tin": 500, "isCelsius": True, "Pout": 2339.19},
        ]
        
        for t in tests:
            Pws = PC.water_vapour_saturation_pressure(T = t["Tin"], isCelsius = t["isCelsius"])
            self.assertTrue(numpy.isclose(Pws, t["Pout"]))
            # print(Pws)
 
    def test_ice_vapour_saturation_pressure(self):
        # https://www.lyotechnology.com/vapor-pressure-of-ice.cfm
        tests = [
            {"Tin": 253.15, "isCelsius": False, "Pout": 103.26},
            {"Tin": -20, "isCelsius": True, "Pout": 103.26}, 
            # {"Tin": 500, "isCelsius": True, "Pout": 2339.19},
        ]
        
        for t in tests:
            Pwi = PC.ice_vapour_saturation_pressure(T = t["Tin"], isCelsius = t["isCelsius"])
            self.assertTrue(numpy.isclose(Pwi, t["Pout"]))
            # print(Pwi)
 

if __name__ == '__main__': 
    verbosity = 1
    
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_calculations)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)
        
            