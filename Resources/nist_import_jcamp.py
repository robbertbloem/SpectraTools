"""

"""

import jcamp
import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import PythonTools.ClassTools as CT

class NistImportJcamp(CT.ClassTools):
    """
    Class to import JCAMP files from nist.gov. (IR spectra).
    
    Attributes
    ----------
    path : Path 
        Path to the file
    filename : Path
        Filename
        
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

        self.verbose = verbose        
        if self.verbose > 1:
            print("NistTools.Resources.nist_import_jcamp.__init__()")           
        if verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))
                
        self.path = kwargs.get("path", None)
        self.filename = kwargs.get("filename", None)
        
        


    def import_file(self, path = None, filename = None):
        """
        
        
        
        Notes
        -----
    
        - 2019-03-03/RB: started function        
        
        """ 
        if self.verbose > 1:
            print("NistTools.Resources.nist_import_jcamp.import_file()")           
        
        if path is not None:
            self.path = path
        
        if filename is not None:
            self.filename = filename
        
        if self.path is None or self.filename is None:
            return None
        
        paf = self.path.joinpath(self.filename)
                
        f = open(paf, "r")
        d = jcamp.jcamp_read(f)
        f.close()        
        
        return d
        
                           



if __name__ == "__main__": 
    pass