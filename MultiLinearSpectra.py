from importlib import reload
import inspect
import os
import warnings

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import PythonTools.ClassTools as CT
import SpectraTools.PAS as PAS
import SpectraTools.PASGas as PASG
import SpectraTools.PASLiquid as PASL

reload(PAS)
reload(PASG)
reload(PASL)
"""
 
INPUT:
- 

OUTPUT:
- 

CHANGELOG:
2019-01-09/RB: started function
"""    
    


class MultiLinearSpectra(CT.ClassTools):
    """
    Class for working on a number of linear spectra.
    
    Variables:
    - mess
    
    Methods:
    + __init__
    + init_data_array
    + import_data
    + select_single_slope
    + get_min_max_x
    + bin_data
    + calculate_signal
    + plot_spectra
    + make_batches
    
    CHANGELOG:
    2019-01-10/RB: started function
    """          
    
    def __init__(self, mess = None, verbose = 0, **kwargs):
        """
         
        INPUT:
        - mess: list with dictionaries. 
            - The dictionary must contain the keyword 'class', this is used to initialize the correct class.
            - The keyword 'object' is reserved for the initialized instance.
            - An index is added (if not already present). This can be used for consistent coloring in plots.
            - Other keywords will be passed as kwargs to the initialization function.
        - verbose:
            - 0: suppress most output
            - >= 1: 
            - >= 2: print function names
            - >= 3: print kwargs
        
        OUTPUT:
        - 
        
        CHANGELOG:
        2019-01-08/RB: started function
        """      
        if verbose > 1:
            print("SpectraTools.MultiLinearSpectra.__init__()")   
        if verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))
        
        self.verbose = verbose

        if mess is not None: 
            self.mess = mess
            self.init_data_array()
            
            
            
    def init_data_array(self, mess = None):
        """
        Initializes lines in mess.  
        
        INPUT:
        - mess: list with dictionaries. 
            - The dictionary must contain the keyword 'class', this is used to initialize the correct class.
            - The keyword 'object' is reserved for the initialized instance.
            - An index is added (if not already present). This can be used for consistent coloring in plots.
            - Other keywords will be passed as kwargs to the initialization function.

        OUTPUT:
        - -

        CHANGELOG:
        2019-01-09/RB: started function
        """  
        if self.verbose > 1:
            print("MultiLinearSpectra.init_data_array()")   
    
        if mess is None:
            if self.mess is None:
                warnings.warn("MultiLinearSpectra.init_data_array(): no data to initialize")
                return None
        else:
            self.mess = mess
    

        
    
        for m in range(len(self.mess)):
        
            self.mess[m]["index"] = m
            
            kwargs = {}
            for k, v in self.mess[m].items():
                kwargs[k] = v
                
            if self.mess[m]["class"] == "PASGas":
                self.mess[m]["object"] = PASG.PASGas(verbose = self.verbose, **kwargs)

            elif self.mess[m]["class"] == "PASLiquid":
                self.mess[m]["object"] = PASL.PASLiquid(verbose = self.verbose, **kwargs)


        # x_unit = self.mess[0].x_unit
        # y_unit = self.mess[0].y_unit

        # for m in range(1, len(self.mess)):
            # if x_unit != self.mess[m].x_unit:
                # self.mess.x_unit

                
    def import_data(self, **kwargs):        
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-01-09/RB: started function
        """  

        if self.verbose > 1:
            print("MultiLinearSpectra.import_data()")       
    
        for m in range(len(self.mess)):
                        
            if self.mess[m]["class"] in ["PASGas", "PASLiquid"]:
                _kwargs = {}
                if "reload" in kwargs:
                    _kwargs["reload"] = kwargs["reload"]
                elif "reload" in self.mess[m]:
                    _kwargs["reload"] = self.mess[m]["reload"]
                
                
                self.mess[m]["object"].import_data(**_kwargs) 

        
            
    def select_single_slope(self, **kwargs):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-01-09/RB: started function
        """  

        if self.verbose > 1:
            print("MultiLinearSpectra.select_single_slope()")   
    
        for m in self.mess:
            if m["class"] == "batch":
                warnings.warn("MultiLinearSpectra.select_single_slope(): slope should be selected before batches are made.")
            
    
        for m in range(len(self.mess)):

            if self.mess[m]["class"] in ["PASGas", "PASLiquid"]:
                
                _kwargs = {}
                
                if "slope" in kwargs:
                    _kwargs["slope"] = kwargs["slope"]
                elif "slope" in self.mess[m]:
                    _kwargs["slope"] = self.mess[m]["slope"]

                if "n" in kwargs:
                    _kwargs["n"] = kwargs["n"]
                elif "n" in self.mess[m]:
                    _kwargs["n"] = self.mess[m]["n"]

                if "axi" in kwargs:
                    _kwargs["axi"] = kwargs["axi"]
                elif "slope" in self.mess[m]:
                    _kwargs["axi"] = self.mess[m]["axi"]                    
            
                self.mess[m]["object"].select_single_slope(**_kwargs)

                
    def get_min_max_x(self, min_x = 1e9, max_x = -1e9, exclude = []):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-01-09/RB: started function
        """  
        
        if self.verbose > 1:
            print("MultiLinearSpectra.get_min_max_x()")   
        
        for m in range(len(self.mess)):
            if m not in exclude and self.mess[m]["class"] not in exclude:
                min_x, max_x = self.mess[m]["object"].get_min_max_x(min_x, max_x)
                # print(self.mess[m]["class"], min_x, max_x)
                
        return min_x, max_x
        
         
    def bin_data(self, x_resolution, min_x = None, max_x = None, exclude = [], **kwargs):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-01-09/RB: started function
        """  

        if self.verbose > 1:
            print("MultiLinearSpectra.make_bins()")   
    
        bins = self.mess[0]["object"].make_bins(x_resolution = x_resolution, min_x = min_x, max_x = max_x) 
    
        for m in range(len(self.mess)):
            if m not in exclude and self.mess[m]["class"] not in exclude:
                if self.mess[m]["class"] in ["PASGas", "PASLiquid", "batch"]:
                    self.mess[m]["object"].bin_data(bins)



                    
    def calculate_signal(self, exclude = [], **kwargs):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-01-09/RB: started function
        """  

        if self.verbose > 1:
            print("MultiLinearSpectra.calculate_signal()")  
    
        for m in range(len(self.mess)):
            if m not in exclude and self.mess[m]["class"] not in exclude:
                if self.mess[m]["class"] in ["PASGas"]:
                    self.mess[m]["object"].calculate_signal()        
         
         
    def plot_spectra(self, exclude = [], axi = None, plot_props = [], **kwargs):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-01-09/RB: started function
        """  

        if self.verbose > 1:
            print("MultiLinearSpectra.plot_spectra()")  
        if self.verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))
                
        if axi is None:
            fig = plt.figure()
            axi = fig.add_subplot(111)
            
        for m in range(len(self.mess)):
            if m not in exclude and self.mess[m]["class"] not in exclude:      
                
                if len(plot_props) > 0:
                    _kwargs = plot_props[m]
                elif "label" in self.mess[m]:
                    _kwargs = {}
                    _kwargs["label"] = self.mess[m]["label"]
                else:
                    _kwargs = {}

                self.mess[m]["object"].plot_spectrum(axi = axi, **_kwargs)

         
         
    def make_batches(self, batches = [], batch_props = None, **kwargs):
        """
         
        INPUT:
        - 

        OUTPUT:
        - 

        CHANGELOG:
        2019-01-09/RB: started function
        2019-01-17/RB: will copy x_unit, checks for empty batches array
        """  
    
        if self.verbose > 1:
            print("MultiLinearSpectra.make_batches()")          
        
        n_mess = len(self.mess)
        
        if len(batches) == 0:
            return None
        
        batch = [{}] * len(batches)
        for b in range(len(batches)):
            batch = {}
            
            if batch_props is not None:
                for k, v in batch_props[b].items():
                    batch[k] = v
            
            batch["index"] = b + n_mess
            batch["class"] = "batch"
            batch["object"] = PAS.PAS(verbose = self.verbose)
            
            batch["object"].x = numpy.array([])
            batch["object"].y = numpy.array([])
            
            x_unit = self.mess[0]["object"].x_unit
            y_unit = self.mess[0]["object"].y_unit

            for m in batches[b]:
                batch["object"].x = numpy.concatenate((batch["object"].x, self.mess[m]["object"].x), axis = 0)
                batch["object"].y = numpy.concatenate((batch["object"].y, self.mess[m]["object"].y), axis = 0)
                
                if x_unit != self.mess[m]["object"].x_unit:
                    warnings.warn("MultiLinearSpectra.make_batches(): inconsistant x_unit")
                    x_unit = None

                if y_unit != self.mess[m]["object"].y_unit:
                    warnings.warn("MultiLinearSpectra.make_batches(): inconsistant y_unit")
                    y_unit = None                    
                    
            batch["object"].x_unit = x_unit
            batch["object"].y_unit = y_unit
                
            self.mess.append(batch)

        
        
        
        

if __name__ == '__main__': 
    pass            