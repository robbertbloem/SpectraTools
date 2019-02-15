import importlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.LinearSpectrum as LS

importlib.reload(LS)

class RefractiveIndex(LS.LinearSpectrum):
    """
    Class for processing refractive indices.
    
    Variables:
    - x
    - n
    - k
    - gvd
    - formula (type)
    - parameters
    - path
    - filename
    
    Methods:
    + init
    + importdata
    + calculate_n
    + calculate_k
    + calculate_gvd
    + calculate_reflection (with air)

    CHANGELOG:
    2019-02-05/RB: started class
    """ 
    def __init__(self, verbose = 0, **kwargs):
        """
        
        2019/02/15-RB: started function
        """
        self.verbose = verbose
        if self.verbose > 1:
            print("RefractiveIndexTools.RefractiveIndexSpectrum.__init__()")           
        if verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))

        if "x" in kwargs:
            self.x = kwargs["x"]            
        else:
            self.x = None

        if "n" in kwargs:
            self.n = kwargs["n"]            
        else:
            self.n = None
            
        if "k" in kwargs:
            self.k = kwargs["k"]            
        else:
            self.k = None

        if "gvd" in kwargs:
            self.gvd = kwargs["gvd"]            
        else:
            self.gvd = None

        if "formula" in kwargs:
            self.formula = kwargs["formula"]            
        else:
            self.formula = None            

        if "parameters" in kwargs:
            self.parameters = kwargs["parameters"]            
        else:
            self.parameters = None    
            
        if "path" in kwargs:
            self.path = kwargs["path"]            
        else:
            self.path = None    

        if "filename" in kwargs:
            self.filename = kwargs["filename"]            
        else:
            self.filename = None                


    def import_data(self):
    
        RIRY.import_refractive_index(paf = paf, verbose = verbose)











            

if __name__ == "__main__": 
    pass