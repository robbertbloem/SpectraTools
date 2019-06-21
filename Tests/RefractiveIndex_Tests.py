import importlib 
import inspect
import os
import warnings
import unittest
import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.RefractiveIndex as RI

importlib.reload(RI)

# path = pathlib.Path(r"C:/Python/Data/refractiveindex/data/")
path = pathlib.Path(r"C:\Python\Data\RefractiveIndexInfo\database\data")

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
        filename = pathlib.Path("main/Ar/Bideau-Mehu.yml")
        RI.RefractiveIndex(verbose = self.verbose, path = path)

class Test_importdata_paths_and_filenames(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
 
    def test_path_filename(self):
        filename = pathlib.Path(r"main/Ar/Bideau-Mehu.yml")
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

    def test_no_path_no_filename_assert_warning(self):
        c = RI.RefractiveIndex(verbose = self.verbose)
        
        with self.assertWarnsRegex(UserWarning, "path and filename"):
            res = c.import_data()
            self.assertTrue(res == 0)

        
    def test_path_no_filename(self):
        c = RI.RefractiveIndex(verbose = self.verbose, path = path)
        with self.assertWarnsRegex(UserWarning, "filename"):
            res = c.import_data()
            self.assertTrue(res == 0)        

    def test_no_path_filename(self):
        filename = pathlib.Path(r"main/Ar/Bideau-Mehu.yml")
        c = RI.RefractiveIndex(verbose = self.verbose, filename = filename)
        with self.assertWarnsRegex(UserWarning, "path"):
            res = c.import_data()
            self.assertTrue(res == 0)            
    
        
        
        
class Test_importdata(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
  
        self.rtol_ri = 0.0001
        self.rtol_gvd = 0.001
        self.atol_gvd = 0.002
        

        self.tab_n_paf = path.joinpath(r"main/Al2O3/Boidin.yml")

        self.mess = [
        # tabulated n
        # https://refractiveindex.info/database/main/Al2O3/Boidin.yml        
        {
            "type": "tabulated n", 
            "filename": pathlib.Path(r"main/Al2O3/Boidin.yml"),
            "range": [0.3, 18.003], 
            # "coefficients": [0, 4.45813734, 0.200859853, 0.467216334, 0.391371166, 2.89566290, 47.1362108],
            "check": [
                {
                    "wl_um": numpy.array([0.30, 7.2822, 18.003]),
                    "ri_check": numpy.array([1.73756, 1.41644, 2.43259]),
                },
                {
                    "wl_um": numpy.array([0.31, 3.1, 13.3]),
                    "ri_check": numpy.array([1.7324, 1.6319, 1.4632]),
                },                     
            ],
        },             
        # tabulated nk
        # https://refractiveindex.info/?shelf=main&book=Ag&page=Babar
        {
            "type": "tabulated nk", 
            "filename": pathlib.Path(r"main/Ag/Babar.yml"),
            "range": [0.2066, 12.4], 
            # "coefficients": [0, 4.45813734, 0.200859853, 0.467216334, 0.391371166, 2.89566290, 47.1362108],
            "check": [
                {
                    "wl_um": numpy.array([0.2066, 0.3999, 8.266]),
                    "ri_check": numpy.array([1.079, 0.054, 3.227]),
                },
                {
                    "wl_um": numpy.array([0.24, 1.2, 10.0]),
                    "ri_check": numpy.array([1.2038, 0.093133, 4.0038]),
                },                
            ],
        },         
        # formula 1
        # https://refractiveindex.info/?shelf=main&book=ZnSe&page=Connolly
        {
            "type": "formula 1", 
            "filename": pathlib.Path(r"main/ZnSe/Connolly.yml"),
            "range": [0.54, 18.2], 
            "coefficients": [0, 4.45813734, 0.200859853, 0.467216334, 0.391371166, 2.89566290, 47.1362108],
            "check": [
                {
                    "wl_um": numpy.array([0.6, 4.0, 5.0, 6.0, 10.0, 18.0]),
                    "ri_check": numpy.array([2.6141, 2.4331, 2.4295, 2.4258, 2.4065, 2.3306]),
                    "gvd_check": numpy.array([2271.1, 75.299, -17.134, -136.21, -1221.0, -14134])
                }
            ],
        },
        # formula 2
        # https://refractiveindex.info/?shelf=main&book=CaF2&page=Daimon-20
       {
            "type": "formula 2", 
            "filename": pathlib.Path(r"main/CaF2/Daimon-20.yml"),
            "range": [0.138, 2.326], 
            "coefficients": [0, 0.443749998, 0.00178027854, 0.444930066, 0.00788536061, 0.150133991, 0.0124119491, 8.85319946, 2752.28175],
            "check": [
                {
                    "wl_um": numpy.array([0.15, 0.4, 0.6, 0.8, 1.5, 2.3]),
                    "ri_check": numpy.array([1.5817, 1.4419, 1.4336, 1.4306, 1.4263, 1.4223]),
                    "gvd_check": numpy.array([846.01, 67.513, 40.230, 27.796, 1.8579, -39.704])
                }
            ],            
        },
        # formula 3
        # https://refractiveindex.info/?shelf=organic&book=benzene&page=Moutzouris
        {
            "type": "formula 3", 
            "filename": pathlib.Path(r"organic/C6H6 - benzene/Moutzouris.yml"),
            "range": [0.450, 1.551], 
            "coefficients": [2.170184597, 0.00059399, 2, 0.02303464, -2, -0.000499485, -4, 0.000178796, -6],
            "check": [
                {
                    "wl_um": numpy.array([0.5, 1.0, 1.5]),
                    "ri_check": numpy.array([1.5053, 1.4810, 1.4770]),
                    "gvd_check": numpy.array([253.85, 81.590, 56.390])
                }
            ],              
        },
        # formula 4
        # https://refractiveindex.info/?shelf=main&book=BaB2O4&page=Eimerl-o
        {
            "type": "formula 4", 
            "filename": pathlib.Path(r"main/BaB2O4/Eimerl-o.yml"),
            "range": [0.22, 1.06], 
            "coefficients": [2.7405, 0.0184, 0, 0.0179, 1, 0, 0, 0, 1, -0.0155, 2],
            "check": [
                {
                    "wl_um": numpy.array([0.25, 0.6, 1.0]),
                    "ri_check": numpy.array([1.7754, 1.6699, 1.6564]),
                    "gvd_check": numpy.array([637.15, 111.14, 45.633])
                }
            ],              
        },
        # formula 5
        # https://refractiveindex.info/?shelf=organic&book=octane&page=Kerl-293K
        {
            "type": "formula 5", 
            "filename": pathlib.Path(r"organic/C8H18 - octane/Kerl-293K.yml"),
            "range": [0.326, 0.644], 
            "coefficients": [1.39260498, -4.48963e-3, -1, 4.79591e-3, -2],
            "check": [
                {
                    "wl_um": numpy.array([0.35, 0.5, 0.63]),
                    "ri_check": numpy.array([1.4189, 1.4028, 1.3976]),
                    "gvd_check": numpy.array([129.69, 86.012, 64.982])
                }
            ],              
        },
        # formula 6
        # https://refractiveindex.info/?shelf=main&book=H2&page=Peck
        {
            "type": "formula 6", 
            "filename": pathlib.Path(r"main/H2/Peck.yml"),
            "range": [0.1680, 1.6945], 
            "coefficients": [0, 0.0148956, 180.7, 0.0049037, 92],
            "check": [
                {
                    "wl_um": numpy.array([0.17, 0.7, 1.2, 1.65]),
                    "ri_check": numpy.array([1.0001874, 1.0001379, 1.0001365, 1.0001361]),
                    "gvd_check": numpy.array([0.22527, 0.016515, 0.010617, 0.0081099])
                }
            ],              
        },
        # formula 6b
        # https://refractiveindex.info/?shelf=main&book=Ar&page=Bideau-Mehu
        {
            "type": "formula 6", 
            "filename": pathlib.Path(r"main/Ar/Bideau-Mehu.yml"),
            "range": [0.1404, 0.5677], 
            "coefficients": [0, 2.50141e-3, 91.012, 5.00283e-4, 87.892, 5.22343e-2, 214.02],
            "check": [
                {
                    "wl_um": numpy.array([0.15, 0.3, 0.4, 0.55]),
                    "ri_check": numpy.array([1.0003733, 1.0002952, 1.0002870, 1.0002823]),
                    "gvd_check": numpy.array([0.40387, 0.068418, 0.046791, 0.030277])
                }
            ],              
        }
        ]
    
    def test_importing(self):
        for m in self.mess:
        
            with self.subTest(m["type"]):
                c = RI.RefractiveIndex(verbose = self.verbose, path = path, filename = m["filename"])
                res = c.import_data() 

                if "type" in m:
                    with self.subTest(m["type"] + " type"):
                        self.assertTrue(c.formula == m["type"])
                 
                if "range" in m:
                    with self.subTest(m["type"] + " range"):   
                        self.assertTrue(numpy.allclose(c.x_range, m["range"]))
                
                if "coefficients" in m:
                    with self.subTest(m["type"] + " coefficients"):   
                        self.assertTrue(numpy.allclose(c.coefficients, m["coefficients"]))    
                
                for check in m["check"]:
                    if "ri_check" in check: 
                        c.x = check["wl_um"]
                        ri = c.get_ri()
                        self.assertTrue(numpy.allclose(ri, check["ri_check"], rtol = self.rtol_ri))

                    if "gvd_check" in check: 
                        c.x = check["wl_um"]
                        gvd = c.get_gvd()
                        self.assertTrue(numpy.allclose(gvd, check["gvd_check"], rtol = self.rtol_gvd, atol = self.atol_gvd))
        
                
                        

    @unittest.expectedFailure
    def test_importing_expected_failure(self):
        for m in self.mess[-1]:
        
            with self.subTest(m["type"]):
                c = RI.RefractiveIndex(verbose = self.verbose, path = path, filename = m["filename"])
                res = c.import_data() 

                if "type" in m:
                    with self.subTest(m["type"] + " type"):
                        self.assertTrue(c.formula == "fiets")
                 
                if "range" in m:
                    with self.subTest(m["type"] + " range"):   
                        self.assertTrue(numpy.allclose(c.x_range, numpy.arange(len(c.x_range))))
                
                if "coefficients" in m:
                    with self.subTest(m["type"] + " coefficients"):   
                        self.assertTrue(numpy.allclose(c.coefficients, numpy.arange(len(c.coefficients))))            

                for check in m["check"]:
                    if "ri_check" in check: 
                        c.x = check["wl_um"]
                        ri = c.get_ri()
                        self.assertTrue(numpy.allclose(ri, numpy.arange(len(ri), rtol = self.rtol_ri)))

                    if "gvd_check" in check: 
                        c.x = check["wl_um"]
                        gvd = c.get_gvd()
                        self.assertTrue(numpy.allclose(gvd, numpy.arange(len(gvd), rtol = self.rtol_gvd, atol = self.atol_gvd)))


class Test_get_dispersive_pulse_broadening(unittest.TestCase):

    def setUp(self):
        self.verbose = 1
        
        self.x = numpy.array([2,3])
        filename = pathlib.Path(r"main/ZnSe/Connolly.yml")
        self.c = RI.RefractiveIndex(verbose = self.verbose, path = path, filename = filename)
        self.c.import_data() 
        
        
        
    def test_t_array_d_array(self):
        
        self.c.x = self.x[:]
        self.c.get_gvd()
        t = numpy.array([50, 100, 150]) 
        d = numpy.array([1,5,10,20])
        res = self.c.get_dispersive_pulse_broadening(t, d)
        self.assertTrue(numpy.all(numpy.shape(res) == numpy.array([2,3,4])))
        
    def test_t_int_d_int(self):
        
        self.c.x = self.x[:]
        self.c.get_gvd()
        t = 50 #numpy.array([50, 100, 150]) 
        d = 10 #numpy.array([1,5,10,20])
        res = self.c.get_dispersive_pulse_broadening(t, d)
        self.assertTrue(numpy.all(numpy.shape(res) == numpy.array([2])))

    def test_t_int_d_array(self):
        
        self.c.x = self.x[:]
        self.c.get_gvd()
        t = 100 
        d = numpy.array([1,5,10,20])
        res = self.c.get_dispersive_pulse_broadening(t, d)
        self.assertTrue(numpy.all(numpy.shape(res) == numpy.array([2,4])))
        
    def test_t_array_d_int(self):
        
        self.c.x = self.x[:]
        self.c.get_gvd()
        t = numpy.array([50, 100, 150]) 
        d = 10
        res = self.c.get_dispersive_pulse_broadening(t, d)
        self.assertTrue(numpy.all(numpy.shape(res) == numpy.array([2,3])))        

        
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

    if 1:
        """
        + get_dispersive_pulse_broadening
        """
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_get_dispersive_pulse_broadening)
        unittest.TextTestRunner(verbosity = verbosity).run(suite)          