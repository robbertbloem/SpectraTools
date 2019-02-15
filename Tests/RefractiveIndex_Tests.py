import importlib 
import inspect
import os
import warnings
import unittest
import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import RefractiveIndexTools.RefractiveIndex as RI

importlib.reload(RI)

path = pathlib.Path(r"C:\\Python\\Data\\refractiveindex\\data\\")

class Test_init(unittest.TestCase):

    def setUp(self):
        self.verbose = 1



    def test_init(self):
        """
        Basic test
        2019-02-05/RB
        """
        c = RI.RefractiveIndex()
        
    def test_init_with_kwargs(self):
        filename = pathlib.Path(r"main\\Ar\\Bideau-Mehu.yml")
        RI.RefractiveIndex(verbose = self.verbose, path = path)

class Test_importdata_paths_and_filenames(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
 
    def test_path_filename(self):
        filename = pathlib.Path(r"main\\Ar\\Bideau-Mehu.yml")
        c = RI.RefractiveIndex(verbose = self.verbose, path = path, filename = filename)
        res = c.import_data()     
        
    def test_no_path_no_filename(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            c = RI.RefractiveIndex(verbose = self.verbose)
            res = c.import_data()
            self.assertTrue(len(w) == 1)
            self.assertTrue(res == 0)
            assert "path" in str(w[-1].message)
            assert "filename" in str(w[-1].message)

    def test_path_no_filename(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            c = RI.RefractiveIndex(verbose = self.verbose, path = path)
            res = c.import_data()
            self.assertTrue(len(w) == 1)
            self.assertTrue(res == 0)  
            assert "filename" in str(w[-1].message)            

    def test_no_path_filename(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            filename = pathlib.Path("Bideau-Mehu.yml")
            c = RI.RefractiveIndex(verbose = self.verbose, filename = filename)
            res = c.import_data()
            self.assertTrue(len(w) == 1)
            self.assertTrue(res == 0)    
            assert "path" in str(w[-1].message)            
    
        
        
        
class Test_importdata(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
  
        self.rtol_ri = 0.0001
        self.rtol_gvd = 0.001
        self.atol_gvd = 0.002
        
        # tabulated n
        # https://refractiveindex.info/database/main/Al2O3/Boidin.yml
        self.tab_n_paf = path.joinpath(r"main\\Al2O3\\Boidin.yml")

        # tabulated nk
        # https://refractiveindex.info/?shelf=main&book=Ag&page=Babar
        self.tab_nk_paf = path.joinpath(r"main\\Ag\\Babar.yml")

        # formula 1
        # https://refractiveindex.info/?shelf=main&book=ZnSe&page=Connolly
        self.f1_paf = path.joinpath(r"main\\ZnSe\\Connolly.yml")
        self.f1 = {
            "type": "formula 1", 
            "range": [0.54, 18.2], 
            "coefficients": [0, 4.45813734, 0.200859853, 0.467216334, 0.391371166, 2.89566290, 47.1362108],
        }

        # formula 2
        # https://refractiveindex.info/?shelf=main&book=CaF2&page=Daimon-20
        self.f2_paf = path.joinpath(r"main\\CaF2\\Daimon-20.yml")
        self.f2 = {
            "type": "formula 2", 
            "range": [0.138, 2.326], 
            "coefficients": [0, 0.443749998, 0.00178027854, 0.444930066, 0.00788536061, 0.150133991, 0.0124119491, 8.85319946, 2752.28175],
        }

        # formula 3
        # https://refractiveindex.info/?shelf=organic&book=benzene&page=Moutzouris
        self.f3_paf = path.joinpath(r"organic\\C6H6 - benzene\\Moutzouris.yml")
        self.f3 = {
            "type": "formula 3", 
            "range": [0.450, 1.551], 
            "coefficients": [2.170184597, 0.00059399, 2, 0.02303464, -2, -0.000499485, -4, 0.000178796, -6],
        }

        # formula 4
        # https://refractiveindex.info/?shelf=main&book=BaB2O4&page=Eimerl-o
        self.f4_paf = path.joinpath(r"main\\BaB2O4\\Eimerl-o.yml")
        self.f4 = {
            "type": "formula 4", 
            "range": [0.22, 1.06], 
            "coefficients": [2.7405, 0.0184, 0, 0.0179, 1, 0, 0, 0, 1, -0.0155, 2],
        }

        # formula 5
        # https://refractiveindex.info/?shelf=organic&book=octane&page=Kerl-293K
        self.f5_paf = path.joinpath(r"organic\\C8H18 - octane\\Kerl-293K.yml")
        self.f5 = {
            "type": "formula 5", 
            "range": [0.326, 0.644], 
            "coefficients": [1.39260498, -4.48963e-3, -1, 4.79591e-3, -2],
        }

        # formula 6
        # https://refractiveindex.info/?shelf=main&book=H2&page=Peck
        self.f6_paf = path.joinpath(r"main\\H2\\Peck.yml")
        self.f6 = {
            "type": "formula 6", 
            "range": [0.1680, 1.6945], 
            "coefficients": [0, 0.0148956, 180.7, 0.0049037, 92],
        }

        # formula 6b
        # https://refractiveindex.info/?shelf=main&book=Ar&page=Bideau-Mehu
        self.f6b_paf = path.joinpath(r"main\\Ar\\Bideau-Mehu.yml")
        self.f6b = {
            "type": "formula 6", 
            "range": [0.1404, 0.5677], 
            "coefficients": [0, 2.50141e-3, 91.012, 5.00283e-4, 87.892, 5.22343e-2, 214.02],
        }
 



        
        
if __name__ == '__main__': 
    verbosity = 1

    
    if 1:
        """
        + __init__
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_init)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)

    if 1:
        """
        + import_data
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_importdata_paths_and_filenames)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)             
        
    if 1:
        """
        + import_data
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_importdata)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)           