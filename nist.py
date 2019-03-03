"""

"""

import importlib
import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import SpectraTools as ST
import SpectraTools.LinearSpectrum as LS

import NistTools.Resources.nist_import_jcamp as NIJ

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
        
    
    def import_data(self):
        """
        
        
        Notes
        -----
    
        - 2019-03-03/RB: started function        
        
        """     
        
        c = NIJ.NistImportJcamp(path = self.path, filename = self.filename)
        self.db_record = c.import_file()           
    




if __name__ == "__main__": 
    pass