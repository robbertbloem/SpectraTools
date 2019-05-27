"""
This is a class-based version of earlier RefractiveIndex based scripts. The data is taken from the website refractiveindex.info. The database should be downloaded and stored locally. 

ALL WAVELENGTHS ARE IN MICRON!!!

test change.

"""


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
 


class RefractiveIndex(LS.LinearSpectrum):
    """
    Class for processing refractive indices.
    
    Attributes
    ----------
    x : ndarray
    x_range : tuple
    n : ndarray
    k : ndarray
    gvd : ndarray
    formula : string
        Which to use for the refractive index calculation
    parameters : dict
    path : string
    filename : string
    

    Notes
    -----
    
    - 2019-02-15/RB: started class
    """ 
    def __init__(self, verbose = 0, **kwargs):
        """
         
        Keyword Arguments
        -----------------
        x : ndarray
        x_range : tuple
        n : ndarray
        k : ndarray
        gvd : ndarray
        formula : string
            Which to use for the refractive index calculation
        parameters : dict
        path : string
        filename : string        


        Notes
        -----
        
        - 2019-02-15/RB: started function
        """    
        self.verbose = verbose
        if self.verbose > 1:
            print("RefractiveIndexTools.RefractiveIndex.__init__()") 
            
        if verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))

        self.x = kwargs.get("x", None)
        self.x_unit = kwargs.get("x_unit", "um")
        self.x_range = kwargs.get("x_range", None)
        self.n = kwargs.get("n", None)
        self.k = kwargs.get("k", None)
        self.gvd = kwargs.get("gvd", None)
        self.formula = kwargs.get("formula", None)
        self.coefficients = kwargs.get("k", None)
        self.db_record = kwargs.get("db_record", None)
        
        
        # if "x" in kwargs:
            # self.x = kwargs["x"]            
        # else:
            # self.x = None

        # if "x_range" in kwargs:
            # self.x_range = kwargs["x_range"]            
        # else:
            # self.x_range = None            
            
        # if "n" in kwargs:
            # self.n = kwargs["n"]            
        # else:
            # self.n = None
            
        # if "k" in kwargs:
            # self.k = kwargs["k"]            
        # else:
            # self.k = None

        # if "gvd" in kwargs:
            # self.gvd = kwargs["gvd"]            
        # else:
            # self.gvd = None

        # if "formula" in kwargs:
            # self.formula = kwargs["formula"]            
        # else:
            # self.formula = None            

        # if "coefficients" in kwargs:
            # self.coefficients = kwargs["coefficients"]            
        # else:
            # self.coefficients = None    

        # if "db_record" in kwargs:
            # self.db_record = kwargs["db_record"]            
        # else:
            # self.db_record = None  
            
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
        Function that imports data and extracts it into a usable format. 

        Notes
        -----
        
        - 2019-02-15/RB: started function
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
        Extract data from the YAML-record format to the class. 

        Notes
        -----
        
        - 2019-02-15/RB: started function
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
        Calls the calculation of the refractive index calculation, after some checks. 

        Notes
        -----
        
        - 2019-02-15/RB: started function
        """   
        if self.verbose > 1:
            print("RefractiveIndex.get_ri()")    
            
        if numpy.amin(self.x) < self.x_range[0]:
            raise ValueError("RefractiveIndex.get_ri(): lowest wavelength is below range.")

        if numpy.amax(self.x) > self.x_range[1]:
            raise ValueError("RefractiveIndex.get_ri(): highest wavelength is above range.")
            
        self.n = RIF.ri(x = self.x, s = self.coefficients, formula = self.formula, verbose = self.verbose)

        return self.n


    def get_k(self):
        """
        Extracts the extinction coefficient, after some checks. 

        Notes
        -----
        
        - 2019-02-15/RB: started function
        """   
        if self.verbose > 1:
            print("RefractiveIndex.get_k()")    
            
        if numpy.amin(self.x) < self.x_range[0]:
            raise ValueError("RefractiveIndex.get_k(): lowest wavelength is below range.")

        if numpy.amax(self.x) > self.x_range[1]:
            raise ValueError("RefractiveIndex.get_k(): highest wavelength is above range.")
            
        self.n = RIF.extinction(x = self.x, s = self.coefficients, formula = self.formula, verbose = self.verbose)

        return self.n        
        
        
    def get_gvd(self):
        """
        Calls the calculation of the group velocity dispersion calculation, after some checks. 

        Notes
        -----
        
        - 2019-02-15/RB: started function
        """   
        if self.verbose > 1:
            print("RefractiveIndex.get_gvd()")    

        if numpy.amin(self.x) < self.x_range[0]:
            raise ValueError("RefractiveIndex.get_gvd(): lowest wavelength is below range.")

        if numpy.amax(self.x) > self.x_range[1]:
            raise ValueError("RefractiveIndex.get_gvd(): highest wavelength is above range.")
            
        gvd = RIF.gvd(x = self.x, s = self.coefficients, formula = self.formula, verbose = self.verbose)
        
        self.gvd = (1e21 * gvd * self.x**3) / (2 * numpy.pi * (CONST.c_ms)**2)
        
        return self.gvd



    def get_dispersive_pulse_broadening(self, t_fs, d_mm):
        """
        Calculates the effect the group velocity dispersion has on an unchirped Gaussian pulse. 

        gvd has to be set (run get_gvd). t_fs and d_mm can be an integer or an array. gvd is always an array (it is the GVD for self.x). The output shape depends on the input:
        
        - t_fs = int, d_mm = int: [x]
        - t_fs = array, d_mm = int: [x, t_fs]
        - t_fs = int, d_mm = array: [x, d_mm]
        - t_fs = array, d_mm = array: [x, t_fs, d_mm]
        
        Arguments
        ---------
        t_fs : number
            pulse durations in fs
        d_mm : number
            thicknesses of material in mm
        
        OUTPUT:
        t_out : ndarray
            1D, 2D, or 3D array with 
        
        Notes
        -----
        
        - 20170315/RB: started function. 
        - 2019-02-15/RB: moved to RefractiveIndexTools
        
        References
        ----------
        
        - The method is taken from `RP Photonics <http://www.rp-photonics.com/chromatic_dispersion.html>`_.
        - numpy.log() is natural log        
        
        """
        if self.verbose > 1:
            print("RefractiveIndex.get_dispersive_pulse_broadening()")    

        if type(t_fs) == int:
            t_fs = CF.make_numpy_ndarray(t_fs)
            t_fs_l = 0
        else:
            t_fs = CF.make_numpy_ndarray(t_fs)
            t_fs_l = len(t_fs)
            
        if type(d_mm) == int:
            d_mm = CF.make_numpy_ndarray(d_mm)  
            d_mm_l = 0
        else:
            d_mm = CF.make_numpy_ndarray(d_mm)  
            d_mm_l = len(d_mm)  
          
        G, T, D = numpy.meshgrid(self.gvd, t_fs, d_mm, indexing = "ij")
        t_out = T * numpy.sqrt(1 + (4 * numpy.log(2) * G * D/ T**2)**2 )

        if t_fs_l == 0 and d_mm_l == 0:
            return t_out[:,0,0]
        elif t_fs_l != 0 and d_mm_l == 0:
            return t_out[:,:,0]
        elif t_fs_l == 0 and d_mm_l != 0:
            return t_out[:,0,:]        
        else:
            return t_out

    def plot_n(self, **kwargs):
        """
        Wrapper around LinearSpectrum.plot_spectrum, to quickly plot the refractive index. 
        
        Kwargs will be passed.
        
        Notes
        -----
        
        - 2019-01-??/RB: started function
        
        """
        if self.verbose > 1:
            print("RefractiveIndex.plot_n()")          

        self.plot_spectrum(y_unit = "Refractive index n", **kwargs)


    def plot_k(self, **kwargs):
        """
        Wrapper around LinearSpectrum.plot_spectrum, to quickly plot the extinction coefficient. 
        
        Kwargs will be passed.
        
        Notes
        -----
        
        - 2019-01-??/RB: started function
        
        """
        if self.verbose > 1:
            print("RefractiveIndex.plot_k()")          

        self.plot_spectrum(y_unit = "Extinction coefficient k", **kwargs)

        
    def plot_gvd(self, **kwargs):
        """
        Wrapper around LinearSpectrum.plot_spectrum, to quickly plot the group velocity dispersion. 
        
        Kwargs will be passed.
        
        Notes
        -----
        
        - 2019-01-??/RB: started function
        
        """
        if self.verbose > 1:
            print("RefractiveIndex.plot_gvd()")          

        self.plot_spectrum(y_unit = r"Group velocity dispersion (fs$^2$/mm)", **kwargs)        

if __name__ == "__main__": 
    pass