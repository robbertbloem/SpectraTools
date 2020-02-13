"""


"""

import pathlib

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import spc

import PythonTools.ClassTools as CT

class SPCImport(CT.ClassTools):
    """
    Class to import SPC files.
    
    Attributes
    ----------
    path : Path 
        Path to the file
    filename : Path
        Filename
        

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

        self.verbose = verbose        
        if self.verbose > 1:
            print("SpectraTools.Resources.spc_import.__init__()")           
        if verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))
                
        self.path = kwargs.get("path", None)
        self.filename = kwargs.get("filename", None)
        
        


    def import_file(self, path = None, filename = None):
        """
        
        

        """ 
        if self.verbose > 1:
            print("SpectraTools.Resources.spc_import.import_file()")           
        
        if path is not None:
            self.path = path
        
        if filename is not None:
            self.filename = filename
        
        if self.path is None or self.filename is None:
            return None
        
        paf = self.path.joinpath(self.filename)
                
        f = open(paf, "r")
        d = spc.File(paf)
        f.close()        
        
        return d
        
                           



if __name__ == "__main__": 
    pass