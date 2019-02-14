from importlib import reload
import inspect
import os
import warnings
import unittest

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.MultiLinearSpectra as MLS

reload(MLS)

plt.close("all")

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 0



    def test_init(self):
        """
        Basic test
        2019-01-07/RB
        """
        P = MLS.MultiLinearSpectra(verbose = self.verbose)


    def test_init_data(self):
        """
        Basic test
        2019-01-07/RB
        """
        mess = [
            {
            "class": "PASGas",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_gas_testdata",
            "filename": "NW1017.ASD",       
            "temperature_channel": 0,
            "audio_channel": 2,
            "pd_channel": 1,
            "temperature_inverted": True,
            "audio_inverted": True,
            },{
            "class": "PASLiquid",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_liquid_testdata",
            "filename": "NW1006.ASD",
            "temperature_channel": 0,
            "audio_channel": 1,
            "temperature_inverted": True,    
            }
        ]

        P = MLS.MultiLinearSpectra(verbose = self.verbose, mess = mess)        
        P.import_data()
        P.select_single_slope()
        min_x, max_x = P.get_min_max_x() 
        P.bin_data(x_resolution = 0.01, min_x = min_x, max_x = max_x)
        P.calculate_signal()
        
        plot_props = [
            {"label": "gas"},
            {"label": "liquid"},
        ]
        
        P.plot_spectra(plot_props = plot_props)
        
        for p in P.mess:
            print(p["object"])
        print(P)
        
        plt.show()
        


class Test_batches(unittest.TestCase):

    def setUp(self):
        self.verbose = 0



    def test_init(self):
        """
        Basic test
        2019-01-07/RB
        """

        gas = {
            "class": "PASGas",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_gas_testdata",
            "filename": "NW1017.ASD",       
            "temperature_channel": 0,
            "audio_channel": 2,
            "pd_channel": 1,
            "temperature_inverted": True,
            "audio_inverted": True,
        }
        liquid = {
            "class": "PASLiquid",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_liquid_testdata",
            "filename": "NW1006.ASD",
            "temperature_channel": 0,
            "audio_channel": 1,
            "temperature_inverted": True,    
        }
        mess = [gas.copy(), gas.copy(), gas.copy(), gas.copy(), liquid.copy(), liquid.copy(), liquid.copy(), liquid.copy(), liquid.copy()]
        mess[0]["filename"] = "NW1017.ASD"
        mess[1]["filename"] = "NW1018.ASD"
        mess[2]["filename"] = "NW1019.ASD"
        mess[3]["filename"] = "NW1020.ASD"
        
        mess[4]["filename"] = "NW1001.ASD"
        mess[5]["filename"] = "NW1002.ASD"
        mess[6]["filename"] = "NW1003.ASD"
        
        mess[7]["filename"] = "NW1004.ASD"
        mess[8]["filename"] = "NW1008.ASD"
        
        self.P = MLS.MultiLinearSpectra(verbose = self.verbose, mess = mess)
        self.P.import_data()
        self.P.select_single_slope()
        min_x, max_x = self.P.get_min_max_x() 
        self.P.bin_data(x_resolution = 0.01, min_x = min_x, max_x = max_x)
        self.P.calculate_signal()        
        
        # plot_props = []
        # for p in range(len(self.P.mess)) :
            # plot_props.append({"label": self.P.mess[p]["filename"]})

        batches = [[0,1,2,3], [4,5,6], [7,8]]
        self.P.make_batches(batches)
            
        # for p in self.P.mess:
            # print(p["object"])
        # print(self.P)            

        # self.P.plot_spectra(plot_props = plot_props)
        
        # plt.show()

    def test_no_batches(self):
        """
        Allows batches-code in script, without actually making batches. 
        2019-01-17/RB
        """

        gas = {
            "class": "PASGas",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_gas_testdata",
            "filename": "NW1017.ASD",       
            "temperature_channel": 0,
            "audio_channel": 2,
            "pd_channel": 1,
            "temperature_inverted": True,
            "audio_inverted": True,
        }
        liquid = {
            "class": "PASLiquid",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_liquid_testdata",
            "filename": "NW1006.ASD",
            "temperature_channel": 0,
            "audio_channel": 1,
            "temperature_inverted": True,    
        }
        mess = [gas.copy(), gas.copy(), gas.copy(), gas.copy(), liquid.copy(), liquid.copy(), liquid.copy(), liquid.copy(), liquid.copy()]
        mess[0]["filename"] = "NW1017.ASD"
        mess[1]["filename"] = "NW1018.ASD"
        mess[2]["filename"] = "NW1019.ASD"
        mess[3]["filename"] = "NW1020.ASD"
        
        mess[4]["filename"] = "NW1001.ASD"
        mess[5]["filename"] = "NW1002.ASD"
        mess[6]["filename"] = "NW1003.ASD"
        
        mess[7]["filename"] = "NW1004.ASD"
        mess[8]["filename"] = "NW1008.ASD"
        
        self.P = MLS.MultiLinearSpectra(verbose = self.verbose, mess = mess)
        self.P.import_data()
        self.P.select_single_slope()
        min_x, max_x = self.P.get_min_max_x() 
        self.P.bin_data(x_resolution = 0.01, min_x = min_x, max_x = max_x)
        self.P.calculate_signal()        

        batches = []
        self.P.make_batches(batches)
            

        
    def test_batch_units_inconsistent(self):
        """
        If batches 
        2019-01-17/RB
        """

        gas = {
            "class": "PASGas",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_gas_testdata",
            "filename": "NW1017.ASD",       
            "temperature_channel": 0,
            "audio_channel": 2,
            "pd_channel": 1,
            "temperature_inverted": True,
            "audio_inverted": True,
        }
        liquid = {
            "class": "PASLiquid",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_liquid_testdata",
            "filename": "NW1006.ASD",
            "temperature_channel": 0,
            "audio_channel": 1,
            "temperature_inverted": True,    
        }
        mess = [gas, liquid]

        self.P = MLS.MultiLinearSpectra(verbose = self.verbose, mess = mess)
        self.P.import_data()
        self.P.select_single_slope()
        min_x, max_x = self.P.get_min_max_x() 
        self.P.bin_data(x_resolution = 0.01, min_x = min_x, max_x = max_x)
        self.P.calculate_signal()        

        batches = [[0,1]]
        self.P.make_batches(batches)

        self.assertTrue(self.P.mess[-1]["object"].x_unit == "cm-1")
        self.assertTrue(self.P.mess[-1]["object"].y_unit is None)
        
        
    def test_batch_units_none(self):
        """
        Basic test
        2019-01-17/RB
        """

        gas = {
            "class": "PASGas",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_gas_testdata",
            "filename": "NW1017.ASD",       
            "temperature_channel": 0,
            "audio_channel": 2,
            "pd_channel": 1,
            "temperature_inverted": True,
            "audio_inverted": True,
        }
        liquid = {
            "class": "PASLiquid",
            "path": "C:\\Python\\SpectraTools\\Tests\\PAS_liquid_testdata",
            "filename": "NW1006.ASD",
            "temperature_channel": 0,
            "audio_channel": 1,
            "temperature_inverted": True,    
        }
        mess = [gas, liquid, liquid, liquid]

        self.P = MLS.MultiLinearSpectra(verbose = self.verbose, mess = mess)
        self.P.import_data()
        self.P.select_single_slope()
        min_x, max_x = self.P.get_min_max_x() 
        self.P.bin_data(x_resolution = 0.01, min_x = min_x, max_x = max_x)
        self.P.calculate_signal()        
        self.P.mess[1]["object"].x_unit = None
        batches = [[0,1]]
        self.P.make_batches(batches)

        self.assertTrue(self.P.mess[-1]["object"].x_unit is None)
        self.assertTrue(self.P.mess[-1]["object"].y_unit is None)
        
if __name__ == '__main__': 

    verbosity = 1
    
    if 0:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)      

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_batches)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)     
        
        
        

        
     