"""
SPC is a file format from Galactic Industries, also known as the Galactic Universal Data Format. 

There are different versions: new and old. EPA uses the old format. EPA uses the old format. It is not as well-defined as the new format. 

The format -- at least for the EPA data -- uses a single x-axis and a list with 1 or more objects that are the y-axes. For the EPA data this list is 2 objects, but only the first object is correct. The second object has a single value for y. 

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
    
    
    def __init__(self, path = None, filename = None, verbose = 0, **kwargs):
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
        
        self.path = path
        self.filename = filename
        
        # self.path = kwargs.get("path", None)
        # self.filename = kwargs.get("filename", None)
        
    
    def import_data(self, load_all = False):
        """
        Import the data. 
        
        self.path and self.filename should have been set. 

        Arguments
        ---------
        load_all : Bool
            Delete the imported SPC object. If True, the SPC object is retained, if False, it is deleted. This saves space. 
        
    
        
        """     
        if self.verbose > 1:
            print("SpectraTools.epa_spectra.import_data()")  

        if self.path is None: 
            raise KeyError("SpectraTools.epa_spectra.import_data(): No path is given.")
        if self.filename is None:
            raise KeyError("SpectraTools.epa_spectra.import_data(): No filename is given.")
                    
        c = SPC.SPCImport(path = self.path, filename = self.filename)
        self.spc_record = c.import_file()        
        self.extract_data_from_spc(load_all = load_all)  

        
        
        
    def extract_data_from_spc(self, load_all = False):
        """
        Extract the data from the spc file into something usable for this class.
        
        Arguments
        ---------
        load_all : Bool
            Delete the imported SPC object. If True, the SPC object is retained, if False, it is deleted. This saves space. 
            
        """
        if self.verbose > 1:
            print("SpectraTools.epa_spectra.extract_data_from_spc()")         
        
        
        self.x = self.spc_record.x
        self.y = self.spc_record.sub[0].y
        
        if self.spc_record.xlabel == "Wavenumber (cm-1)":
            self.x_unit = "cm-1"
            
        if self.spc_record.ylabel == "Absorbance":
            self.y_unit = "A"
            
        self.comment = self.spc_record.ocmnt.decode("utf-8")
        
        if load_all == False:
            self.spc_record = 0
        
        # for key in sorted(self.spc_record.__dict__):
            # print(key, getattr(self.spc_record, key))        
            

                
        
        
        
        

        