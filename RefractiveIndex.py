import importlib
import pathlib
import warnings

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import PythonTools.Constants as CONST
import PythonTools.CommonFunctions as CF
import SpectraTools.LinearSpectrum as LS
import RefractiveIndexTools.Resources.RI_read_yaml as RIRY
import RefractiveIndexTools.Resources.RI_Functions as RIF

importlib.reload(CONST)
importlib.reload(LS)
importlib.reload(RIRY)
importlib.reload(RIF)
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
    - x_range
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

        if "x_range" in kwargs:
            self.x_range = kwargs["x_range"]            
        else:
            self.x_range = None            
            
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

        if "coefficients" in kwargs:
            self.coefficients = kwargs["coefficients"]            
        else:
            self.coefficients = None    

        if "db_record" in kwargs:
            self.db_record = kwargs["db_record"]            
        else:
            self.db_record = None  
            
        if "path" in kwargs:
            if type(kwargs["path"]) in [pathlib.Path, pathlib.WindowsPath, pathlib.PosixPath]:
                self.path = kwargs["path"]
            elif type(kwargs["path"]) == str:
                self.path = pathlib.Path(kwargs["path"])
            else:  
                self.path = None   
                warnings.warn("RefractiveIndex.__init__(): path should either be a pathlib.Path or a string") #.format(type(kwargs["path"]))
        else:
            self.path = None    

        if "filename" in kwargs:
            if type(kwargs["filename"]) in [pathlib.Path, pathlib.WindowsPath, pathlib.PosixPath]:
                self.filename = kwargs["filename"]
            elif type(kwargs["filename"]) == str:
                self.filename = pathlib.Path(kwargs["filename"])
            else:   
                self.filename = None      
                warnings.warn("RefractiveIndex.__init__(): filename should either be a pathlib.Path or a string") #, not a {:}".format(type(kwargs["filename"]))
        else:
            self.filename = None            


    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if type(value) == tuple:
            self._x = numpy.arange(value[0], value[1])
        else:
            self._x = CF.make_numpy_ndarray(value)

    @x.deleter
    def x(self):
        self._x = None            
            

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
        
        self.db_record = RIRY.import_refractive_index(paf = paf, verbose = self.verbose)
        
        self.extract_data_from_db_record()
        
        
    def extract_data_from_db_record(self):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-02-15/RB: started function
        """    
        if self.verbose > 1:
            print("RefractiveIndex.extract_data_from_db_record()")        
        
        if "type" in self.db_record:
            self.formula = self.db_record["type"]

        if "coefficients" in self.db_record:
            self.coefficients = self.db_record["coefficients"]
            
        if "data" in self.db_record:
            self.coefficients = self.db_record["data"]

        if "range" in self.db_record:
            self.x_range = self.db_record["range"]
        elif "data" in self.db_record:
            self.x_range = [numpy.amin(self.db_record["data"][:,0]), numpy.amax(self.db_record["data"][:,0])]
            
    def get_ri(self):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-02-15/RB: started function
        """   
        if self.verbose > 1:
            print("RefractiveIndex.get_ri()")    

        # if wl_um is None and self.x is None:
            # raise ValueError("RefractiveIndex.get_ri(): no wavelengths to calculate the refractive index for.")
  
        # elif wl_um is not None:
            # self.x = wl_um
            
        # elif self.x is None:            
            
            
        if numpy.amin(self.x) < self.x_range[0]:
            raise ValueError("RefractiveIndex.get_ri(): lowest wavelength is below range.")

        if numpy.amax(self.x) > self.x_range[1]:
            raise ValueError("RefractiveIndex.get_ri(): highest wavelength is above range.")
            
        ri = RIF.ri(x = self.x, s = self.coefficients, formula = self.formula, verbose = self.verbose)
        
        return ri


    def get_gvd(self):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-02-15/RB: started function
        """   
        if self.verbose > 1:
            print("RefractiveIndex.get_gvd()")    

        if numpy.amin(self.x) < self.x_range[0]:
            raise ValueError("RefractiveIndex.get_gvd(): lowest wavelength is below range.")

        if numpy.amax(self.x) > self.x_range[1]:
            raise ValueError("RefractiveIndex.get_gvd(): highest wavelength is above range.")
            
        gvd = RIF.gvd(x = self.x, s = self.coefficients, formula = self.formula, verbose = self.verbose)
        
        gvd = (1e21 * gvd * self.x**3) / (2 * numpy.pi * (CONST.c_ms)**2)
        
        return gvd




            

if __name__ == "__main__": 
    pass