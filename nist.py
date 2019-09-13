"""

"""

import importlib
import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools as ST
import SpectraTools.LinearSpectrum as LS

import SpectraTools.Resources.nist_import_jcamp as NIJ

importlib.reload(LS)
importlib.reload(NIJ)

class nist(LS.LinearSpectrum):
    """
    
    Attributes
    ----------

        
    Notes
    -----
    
    - 2019-03-03/RB: started class
    
    """
    
    
    def __init__(self, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        path : Path 
            Path to the file
        filename : Path
            Filename
        
        Notes
        -----
    
        - 2019-03-03/RB: started function        
        
        """
          
        LS.LinearSpectrum.__init__(self, verbose = verbose, **kwargs)    
        if self.verbose > 1:
            print("NistTools.nist.__init__()")           
        if verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))        
        
        self.path = kwargs.get("path", None)
        self.filename = kwargs.get("filename", None)
        
    
    def import_data(self, suppress_unit_warning = False):
        """
        Import the data. 
        
        self.path and self.filename should have been set. 
        
        Notes
        -----
    
        - 2019-03-03/RB: started function        
        
        """     
        if self.verbose > 1:
            print("NistTools.nist.import_data()")   
                    
        c = NIJ.NistImportJcamp(path = self.path, filename = self.filename)
        self.db_record = c.import_file()        
        self.extract_data_from_db_record(suppress_unit_warning = suppress_unit_warning)   
    
    
    
    def extract_data_from_db_record(self, suppress_unit_warning = False):
        """
        Extract the data from the nist file into something usable for this class.
        
        Notes
        -----
    
        - 2019-03-03/RB: started function        
        
        """  
        if self.verbose > 1:
            print("NistTools.nist.extract_data_from_db_record()")   
        
        if "x" in self.db_record:
            self.x = self.db_record.pop("x")

        if "y" in self.db_record:
            self.y = self.db_record.pop("y")

        
        if "xunits" in self.db_record:
            if self.db_record["xunits"] == "1/CM":
                self.x_unit = "wavenumber"
            else:   
                print("NistTools.nist.extract_data_from_db_record(): {:} is an unknown (or not implemented) unit for x".format(self.db_record["xunits"]))  
                
        if "yunits" in self.db_record:
            if self.db_record["yunits"] == "TRANSMITTANCE":
                self.y_unit = "T1"
            else:   
                print("NistTools.nist.extract_data_from_db_record(): {:} is an unknown (or not implemented) unit for y".format(self.db_record["yunits"]))             
        
        
                
        




if __name__ == "__main__": 
    pass