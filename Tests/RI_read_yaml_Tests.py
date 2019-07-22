
import unittest
import pathlib

import importlib

import numpy

import SpectraTools.Resources.RI_read_yaml as RIRY

importlib.reload(RIRY)



class Test_coefficient_file(unittest.TestCase):

    def setUp(self):
        self.flag_verbose = 0

    def test_import_file_simple(self):
        paf = "C:\\Python\\Data\\RefractiveIndexInfo\\database\\data\\main\\CaF2\\Daimon-20.yml"
        out = RIRY.import_refractive_index(paf, verbose = self.flag_verbose)
        
    def test_import_file_path_as_string(self):
        paf = "C:\\Python\\Data\\RefractiveIndexInfo\\database\\data\\main\\CaF2\\Daimon-20.yml"
        out = RIRY.import_refractive_index(paf, verbose = self.flag_verbose)
        
        check = [0, 0.443749998, 0.00178027854, 0.444930066, 0.00788536061, 0.150133991, 0.0124119491, 8.85319946, 2752.28175]
        self.assertTrue(numpy.allclose(out["coefficients"], check))
        
        check = "formula 2"
        self.assertTrue(out["type"] == check)

        self.assertTrue(out["range"][0] == 0.138)
        self.assertTrue(out["range"][1] == 2.326)

    def test_import_file_pathlib(self):
        paf = pathlib.Path(r"C:\\Python\\Data\\RefractiveIndexInfo\\database\\data\\main\\CaF2\\Daimon-20.yml")
        out = RIRY.import_refractive_index(paf, verbose = self.flag_verbose)
        
        check = [0, 0.443749998, 0.00178027854, 0.444930066, 0.00788536061, 0.150133991, 0.0124119491, 8.85319946, 2752.28175]
        self.assertTrue(numpy.allclose(out["coefficients"], check))
        
        check = "formula 2"
        self.assertTrue(out["type"] == check)

        self.assertTrue(out["range"][0] == 0.138)
        self.assertTrue(out["range"][1] == 2.326)

        

class Test_data_n_file(unittest.TestCase):

    def setUp(self):
        self.flag_verbose = 1

    def test_import_file(self):
        paf = "C:\\Python\\Data\\RefractiveIndexInfo\\database\\data\\main\\Al2O3\\Boidin.yml"
        out = RIRY.import_refractive_index(paf, verbose = 0)
        
#         for i in out:
#             print(i, "->", out[i])      

        check = [0.3, 1.73756]
        self.assertTrue(numpy.allclose(out["data"][0], check))

        check = "tabulated n"
        self.assertTrue(out["type"] == check)
        
        
class Test_data_nk_file(unittest.TestCase):

    def setUp(self):
        self.flag_verbose = 1

    def test_import_file(self):
        paf = "C:\\Python\\Data\\RefractiveIndexInfo\\database\\data\\main\\Ag\\Babar.yml"
        out = RIRY.import_refractive_index(paf, verbose = 0)
        
        check = [0.2066, 1.079, 1.247]
        self.assertTrue(numpy.allclose(out["data"][0], check))

        check = "tabulated nk"
        self.assertTrue(out["type"] == check)


    
    def test_import_file_wrong_type_data(self):
        paf = "C:\\Python\\Data\\RefractiveIndexInfo\\database\\data\\main\\Ag\\Babar.yml"
        out = RIRY.import_refractive_index(paf, verbose = 0)
        
        check = [0.21, 1.079, 1.247]
        self.assertFalse(numpy.allclose(out["data"][0], check))

        check = "tabulated n"
        self.assertFalse(out["type"] == check)       



class Test_string_to_ncol(unittest.TestCase):
    """
    The conversion from string to an ndarray is done in CommonFunctions and is tested there. These tests are to make sure that conversion from 1D-array to multidimensional array is done properly. 
    
    """


    def setUp(self):
        self.flag_verbose = 1


    def test_1col(self):
        """
        Most basic use of function.
        """
        data = "0 0.443749998 0.00178027854 0.444930066 0.00788536061 0.150133991 0.0124119491 8.85319946 2752.28175"
        out = RIRY.string_to_cols(data, ncols = 1)  
        check = [0, 0.443749998, 0.00178027854, 0.444930066, 0.00788536061, 0.150133991, 0.0124119491, 8.85319946, 2752.28175]
        self.assertTrue(numpy.allclose(out, check))


    def test_2col(self):
        """
        Most basic use of function.
        """
        data = "0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0"
        out = RIRY.string_to_cols(data, ncols = 2)  
        check = [
            [0.0, 1.0],
            [2.0, 3.0],
            [4.0, 5.0],
            [6.0, 7.0]
        ]
        self.assertTrue(numpy.allclose(out, check))

    def test_3col(self):
        """
        Most basic use of function.
        """
        data = "0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8"
        out = RIRY.string_to_cols(data, ncols = 3)  
        check = [
            [0.0, 1.0, 2.0],
            [3.0, 4.0, 5.0],
            [6.0, 7.0, 8.0]
        ]
        self.assertTrue(numpy.allclose(out, check))





if __name__ == '__main__': 
    verbosity = 0
    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_coefficient_file)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)     

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_data_n_file)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)     

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_data_nk_file)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)     

    if 1:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_string_to_ncol)
        unittest.TextTestRunner(verbosity=verbosity).run(suite)     

 















