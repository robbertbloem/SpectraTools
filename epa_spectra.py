"""

"""

import importlib
import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools as ST
import SpectraTools.LinearSpectrum as LS
import SpectraTools.Resources.spc_import as SPC

importlib.reload(LS)
importlib.reload(SPC)

class epa_spectra(LS.LinearSpectrum):
    """
    
    Attributes
    ----------

        

    
    """
    
    
    def __init__(self, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        path : Path 
            Path to the file
        filename : Path
            Filename
        

        """
          
        LS.LinearSpectrum.__init__(self, verbose = verbose, **kwargs)    
        if self.verbose > 1:
            print("SpectraTools.epa_spectra.__init__()")           
        if verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))        
        
        self.path = kwargs.get("path", None)
        self.filename = kwargs.get("filename", None)
        
    
    def import_data(self, x_unit = None, y_unit = None):
        """
        Import the data. 
        
        self.path and self.filename should have been set. 

        Arguments
        ---------
        x_unit : str (optional, None)
            The x_unit is normally given in the file. Use this to override that.
        y_unit : str (optional, None)
            The y_unit is normally given in the file. Use this to override that.
        
    
        
        """     
        if self.verbose > 1:
            print("SpectraTools.epa_spectra.import_data()")   
                    
        c = SPC.SPCImport(path = self.path, filename = self.filename)
        self.spc_record = c.import_file()        
        self.extract_data_from_spc(x_unit = x_unit, y_unit = y_unit)  

        
        
        
    def extract_data_from_spc(self, x_unit = None, y_unit = None):
        """
        Extract the data from the spc file into something usable for this class.
        
        Arguments
        ---------
        x_unit : str (optional, None)
            The x_unit is normally given in the file. Use this to override that.
        y_unit : str (optional, None)
            The y_unit is normally given in the file. Use this to override that.
            
        """
        if self.verbose > 1:
            print("SpectraTools.epa_spectra.extract_data_from_spc()")         
        
        
        
        
        

        