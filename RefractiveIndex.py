import importlib
import pathlib
import warnings

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools.LinearSpectrum as LS

importlib.reload(LS)

"""
 
INPUT:
- 

OUTPUT:
- 

CHANGELOG:
2019-02-15/RB: started function
"""    


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
    2019-02-15/RB: started class
    """ 
    def __init__(self, verbose = 0, **kwargs):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-02-15/RB: started function
        """    
        self.verbose = verbose
        if self.verbose > 1:
            print("RefractiveIndexTools.RefractiveIndex.__init__()")           
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
            self.path = pathlib.Path(kwargs["path"])
        else:
            self.path = None    

        if "filename" in kwargs:
            self.filename = pathlib.Path(kwargs["filename"])
        else:
            self.filename = None                


    def import_data(self):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-02-15/RB: started function
        """    
        if self.verbose > 1:
            print("RefractiveIndex.import_data()")
        
        if self.path is None and self.filename is None:
            warnings.warn("RefractiveIndex.import_data(): path and filename are not defined.")
            return 0
        elif self.path is None:
            warnings.warn("RefractiveIndex.import_data(): path is not defined.")
            return 0
        elif self.filename is None:
            if self.path.suffix == "yml":
                paf = self.path
            else:
                warnings.warn("RefractiveIndex.import_data(): filename is not defined.")
                return 0
        else:
            paf = self.path.joinpath(self.filename)
        
        # self.db_record = RIRY.import_refractive_index(paf = paf, verbose = verbose)
        
        
        











            

if __name__ == "__main__": 
    pass