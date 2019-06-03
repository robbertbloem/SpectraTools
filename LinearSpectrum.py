"""
This is the main class for linear spectra. 

"""


import importlib 
import inspect
import os
import warnings

import numpy
import matplotlib 
import matplotlib.pyplot as plt

import PythonTools.ClassTools as CT
import PythonTools.CommonFunctions as CF
import PythonTools.Mathematics as MATH
import SpectraTools.Resources.CommonFunctions as ST_CF

importlib.reload(CT)
importlib.reload(CF)
importlib.reload(MATH)
importlib.reload(ST_CF)



class LinearSpectrum(CT.ClassTools):
    """
    Class for linear spectra. Contains basic methods. Is usually subclassed. 
    
    Attributes
    ----------
    x : ndarray
        The x-axis.
    y : ndarray
        The values for x
    x_unit : str
        The unit of the x-axis
    y_unit : str
        The unit of the y-axis
    
    
    """      
#     - 2019-01-03/RB: started class
    
    def __init__(self, verbose = 0, **kwargs):

        """
         
        Keyword Arguments
        -----------------
        x : ndarray
            The x-axis.
        y : ndarray
            The values for x
        x_unit : str
            The unit of the x-axis
        y_unit : str
            The unit of the y-axis
        
        """      
#         - 2019-01-04/RB: started function
        
        self.verbose = verbose
        if self.verbose > 1:
            print("SpectraTools.LinearSpectrum.__init__()")           
        if verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))

        self.x = kwargs.get("x", None)
        self.x_unit = kwargs.get("x_unit", "")
        self.y = kwargs.get("y", None)
        self.y_unit = kwargs.get("y_unit", "")
        
        # if "x" in kwargs:
            # self.x = kwargs["x"]            
        # else:
            # self.x = None
            
        # if "y" in kwargs:
            # self.y = kwargs["y"]
        # else:
            # self.y = None

        # if "x_unit" in kwargs:
            # self.x_unit = kwargs["x_unit"]
        # else:
            # self.x_unit = ""

        # if "y_unit" in kwargs:
            # self.y_unit = kwargs["y_unit"]
        # else:
            # self.y_unit = ""


        self.nm_labels = ["nm"]
        self.um_labels = ["um", "micron"]
        self.cm_labels = ["cm-1", "wavenumber"]
        self.ev_labels = ["ev", "eV"]
            
        self.absorption_labels = ["A"]
        self.transmission_1_labels = ["T1"]
        self.transmission_pct_labels = ["T100"]            

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        self._x = None
            
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @y.deleter
    def y(self):
        self._y = None

    def make_bins(self, x_resolution, min_x = None, max_x = None):
        """
        .. deprecated:: 0.2
            Use `make_new_x` instead.
        
        Make bins, given the resolution for x. The values are the center of the bin. This function does not do the actual binning: use bin_data for that.
        
        Caution: the binning starts at the first index. The last bin is most likely partial.
        
        Arguments
        ---------
        x_resolution : float
            required resolution
        
        Returns
        -------
        new_x : ndarray
            the bins for x. 
        
        """    
#         - 2019-01-04/RB: started function
#         - 2019-02-26/RB: moved functionality to make_new_x. 
        
        print("LinearSpectrum:make_bins(): DEPRECATED")        
        self.make_bins(x_resolution = x_resolution, min_x = min_x, max_x = max_x)
        
            
    def make_new_x(self, x_resolution, min_x = None, max_x = None):
        """
        Make a new x axis, for binning or interpolation. It uses the resolution for x. The values are the center of the bin. This function does not do the actual binning: use bin_data for that.
        
        Caution: the binning starts at the first index. The last bin is most likely partial.
        
        Arguments
        ---------
        x_resolution : float
            required resolution
        
        Returns
        -------
        new_x : ndarray
            the bins for x.  

        """               
#         - 2019-01-04/RB: started function
#         - 2019-02-26/RB: renamed function make_new_x to make it more applicable for interpolation.

        if self.verbose > 1:
            print("LinearSpectrum:make_bins()")
        
        if min_x is None and max_x is None:
            if self.x is None:
                return None
                
        if min_x is not None:
            start = min_x + x_resolution / 2
        else:
            start = numpy.amin(self.x) + x_resolution / 2

        if max_x is not None:
            end = max_x + x_resolution / 10
        else:
            end = numpy.amax(self.x) + x_resolution / 10
            
        return numpy.arange(start, end, x_resolution)

        
    def get_min_max_x(self, min_x = 1e9, max_x = -1e9):
        """
        Get the minimum and maximum value of x. By using the output of this function as the input for this function with another dataset, the minimum and maximum wavenumber for a set of data can be found. This can be used to make bins for all data. 
        
        Arguments
        ---------
        min_x : float
            Default: 1e9
        max_x : float
            Default: -1e9
        
        Returns
        -------
        min_x,max_x : float
        

        """
#         - 2018-12-12/RB: started function
#         - 2019-01-08/RB: moved function to LinearSpectrum

        if self.verbose > 1:
            print("LinearSpectrum.get_min_max_x()")    
            
        if numpy.amin(self.x) < min_x:
            min_x = numpy.amin(self.x)
        if numpy.amax(self.x) > max_x:
            max_x = numpy.amax(self.x)   
        return min_x, max_x        


    def find_indices_for_cropping(self, min_x = None, max_x = None, x = None, pad = 5, crop_index = False):
        """
        Find the indices between min_x and max_x and pad them. min_x and/or max_x has to be given. min_x and max_x can be outside the values of x, but the function returns a warning if no indices are found. 
        
        x has to ascending or descending. 
        
        Arguments
        ---------
        min_x : number, optional 
        max_x : number, optional
        x : ndarray, optional
            if x is given, it is used instead of self.x
        pad : number (5)
            Default: 5
        crop_index : bool (False)
            If True, min_x and max_x are considered as indices. Otherwise, they are considered to be values. 
        
        
        Returns
        -------
        idx : ndarray 
            Indices to be used
        
        
        """
#         - 2019-01-08/RB: started function
           
        if self.verbose > 1:
            print("LinearSpectrum:find_indices_for_cropping()")        
            
        if x is None:
            if self.x is None:
                warnings.warn("LinearSpectrum.find_indices_for_cropping(): no x data")
                return None
            else:
                x = self.x

        if crop_index == False:
            if min_x is not None and max_x is not None:
                if min_x > max_x:
                    temp = max_x
                    max_x = min_x
                    min_x = temp            
                idx = numpy.where(numpy.logical_and(x >= min_x, x <= max_x))[0]
            elif min_x is not None:
                idx = numpy.where(x > min_x)[0]
            elif max_x is not None:
                idx = numpy.where(x < max_x)[0]    
            else:
                return None
        else:
            if min_x > max_x:
                temp = max_x
                max_x = min_x
                min_x = temp    
            if type(min_x) != int:
                min_x = int(min_x)
            if type(max_x) != int:
                max_x = int(max_x)                
            idx = numpy.arange(min_x, max_x + 1)
                
        
        if len(idx) == 0:
            warnings.warn("LinearSpectrum.find_indices_for_cropping(): array ({:}-{:}) does not contain values in the range {:}-{:}".format(x[0], x[-1], min_x, max_x))
            return None
        
        if type(pad) != int:
            pad = 5
        if pad < 1:
            pad = 1
        
        idx = numpy.insert(idx, 0, numpy.arange(idx[0] - pad, idx[0]))         
        idx = numpy.append(idx, numpy.arange(idx[-1] + 1, idx[-1] + pad + 1))  
        temp = numpy.where(numpy.logical_and(idx >= 0, idx < len(x)))[0]
        idx = idx[temp] 
            
        return idx


    
    def bin_data_helper(self, new_x, y = None):
        """
        Take data and bin it. By default self.y is binned, unless y is given in the function parameters. 
        self.x and self.y are not changed in this function. 
        
        Arguments
        ---------
        new_x : ndarray
        y : ndarray, optional 
            If not given, use self.y. y can be 1 dimension, or 2 dimensions (cols x data). 
        
        Returns
        -------
        new_x : ndarray
        new_y : ndarray
        

        """      
#         - 2019-01-04/RB: started function
#         - 2019-01-08/RB: return both new_x and new_y
#         - 2019-02-27/RB: 
#             - moved the mapping between x and new_x to another function. 
#             - if y is 1 dimensional, new_y is as well
        
                   
        if self.verbose > 1:
            print("LinearSpectrum.bin_data()")            
        
        # use y, or self.y, or give an error
        if y is None:
            if self.y is None: 
                warnings.warn("LinearSpectrum.bin_data(): no data to bin")
                return None
            else:
                y = self.y[:]

        digitized = ST_CF.indices_for_binning(self.x, new_x)

        dim = len(numpy.shape(y))
        if dim == 1:
            y = numpy.reshape(y, (1, len(y)))        
        n_y = numpy.shape(y)[0]
        new_y = numpy.zeros((n_y, len(new_x)))     
        empty_bin_count = 0
        for b in range(len(new_x)):
            temp = y[:, digitized == b]
            if numpy.shape(temp)[1] == 0:
                new_y[:,b] = numpy.nan
                empty_bin_count += 1                    
            else:
                new_y[:, b] = temp.mean(axis = 1)         
        
        if dim == 1:    
            new_y = new_y[0,:]
        
        if self.verbose > 0:
            print("LinearSpectrum : bin_data: Number of empty bins: {:d}".format(empty_bin_count))

        return new_x, new_y

    def bin_data(self, new_x = None, x_resolution = None):    
        """
        This function provides the most basic binning functionality: self.y. In most cases this has to be sub-classed.  
        
        """
#         - 2019-01-09/RB: started function
           
        if self.verbose > 1:
            print("LinearSpectra.bin_data()")         
        
        if new_x is None:
            if x_resolution is None:
                return None
            else:
                new_x = self.make_bins(x_resolution)

        self.x, y = self.bin_data_helper(new_x, self.y)
        
        self.y = y


    def interpolate_data_helper(self, new_x = None, x_resolution = None):
        """
         

        
        """    
#         - 2019-02-26/RB: started function

        if self.verbose > 1:
            print("LinearSpectra.interpolate_data_helper()") 

        if new_x is None:
            if x_resolution is None:
                return None
            else:
                new_x = self.make_bins(x_resolution)            
            
        y = MATH.interpolate_data(self.x, self.y, new_x, interpolate_kind = "default", verbose = self.verbose)
        
        return y
        
    def interpolate_data(self, new_x = None, x_resolution = None):
        """
        Placeholder function.
       
        """     
#          - 2019-02-26/RB: started function
        
        if self.verbose > 1:
            print("LinearSpectra.interpolate_data()")         

        y = self.interpolate_data_helper(new_x = new_x, x_resolution = x_resolution)            
        
        return y
        
        
    def crop_x(self, min_x = None, max_x = None, **kwargs):
        """
        Wrapper around LinearSpectra.find_indices_for_cropping().
        
        """           
#         - 2019-01-07/RB: started function
        
        if self.verbose > 1:
            print("LinearSpectra.crop_x()")         
        if self.verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))
                
        idx = self.find_indices_for_cropping(min_x, max_x, **kwargs)

        if idx is None:
            return None
        
        if self.x is not None:
            self.x = self.x[idx]

        if self.y is not None:
            self.y = self.y[idx]            
   
        
        
    def calculate_signal(self):
        """
        Placeholder function. Should be implemented in subclasses, if needed.  

        """
#         - 2019-01-09/RB: started function
             
        if self.verbose > 1:
            print("LinearSpectrum.calculate_signal() -- placeholder")         
        pass

    def import_data(self):
        """
        Placeholder function. Should be implemented in subclasses, if needed.  

        """     
#         - 2019-01-09/RB: started function
        
        if self.verbose > 1:
            print("LinearSpectrum.import_data() -- placeholder")         
        pass        
        
    def convert_x(self, new_unit, x = None, old_unit = ""):
        """
        Convert the x axis from one unit to another. Supported options are nm, micron, wavenumber, and eV. If the old and new unit are the same, or if the new unit is unsupported, then the output will be the same as the input.
        
        self.x will be used, unless x is given in the parameters. self.x and self.x_unit will not be changed. 
        
        Arguments
        ---------
        new_unit : string
            the unit to convert to. 
        x : ndarray, optional
            If given, this array will be converted. Otherwise self.x will be converted.
        old_unit :string (default: "")
            If given, use this as the current unit. Otherwise, self.x_unit will be used. 
        
        Returns
        -------
        new_x : ndarray
        x_unit : string

        """   
#         - 2019-01-04/RB: started function
#         - 2019-01-08/RB: x as input, self.x and self.x_unit are not affected. 

        if self.verbose > 1:
            print("LinearSpectrum.convert_x()") 
            
        if old_unit == "":
            if self.x_unit == "":
                warnings.warn("LinearSpectrum : convert_x: no old unit given")
                return self.x, old_unit
            else:
                old_unit = self.x_unit
        
        if self.x is None and x is None:
            warnings.warn("LinearSpectrum : convert_x: x is not given and can't be converted.")
            return None, old_unit
        elif x is None:
            x = self.x[:]
      

        
        if old_unit in self.nm_labels:
            if new_unit in self.nm_labels:
                x_unit = self.nm_labels[0]
                new_x = x
            elif new_unit in self.um_labels:
                x_unit = self.um_labels[0]
                new_x = x / 1000
            elif new_unit in self.cm_labels:
                x_unit = self.cm_labels[0]
                new_x = 1e7 / x    
            elif new_unit in self.ev_labels:
                x_unit = self.ev_labels[0]
                new_x = 1239.84 / x
            else:
                warnings.warn("LinearSpectrum.convert_x(): new unit ({:s}) is not supported".format(new_unit))
                x_unit = old_unit
                new_x = x
                
        elif old_unit in self.um_labels:
            if new_unit in self.nm_labels:
                x_unit = self.nm_labels[0]
                new_x = x * 1000
            elif new_unit in self.um_labels:
                x_unit = self.um_labels[0]
                new_x = x 
            elif new_unit in self.cm_labels:
                x_unit = self.cm_labels[0]
                new_x = 1e4 / x    
            elif new_unit in self.ev_labels:
                x_unit = self.ev_labels[0]
                new_x = 1.23984 / x
            else:
                warnings.warn("LinearSpectrum.convert_x(): new unit ({:s}) is not supported".format(new_unit))
                x_unit = old_unit
                new_x = x
                
        elif old_unit in self.cm_labels:
            if new_unit in self.nm_labels:
                x_unit = self.nm_labels[0]
                new_x = 1e7 / x
            elif new_unit in self.um_labels:
                x_unit = self.um_labels[0]
                new_x = 1e4 / x 
            elif new_unit in self.cm_labels:
                x_unit = self.cm_labels[0]
                new_x = x    
            elif new_unit in self.ev_labels:
                x_unit = self.ev_labels[0]
                new_x = 1239.84 * x / 1e7
            else:
                warnings.warn("LinearSpectrum.convert_x(): new unit ({:s}) is not supported".format(new_unit))
                x_unit = old_unit
                new_x = x                
        
        elif old_unit in self.ev_labels:
            if new_unit in self.nm_labels:
                x_unit = self.nm_labels[0]
                new_x = 1239.84 / x
            elif new_unit in self.um_labels:
                x_unit = self.um_labels[0]
                new_x = 1.23984 / x
            elif new_unit in self.cm_labels:
                x_unit = self.cm_labels[0]
                new_x = 1e7 * x / 1239.84     
            elif new_unit in self.ev_labels:
                x_unit = self.ev_labels[0]
                new_x = x
            else:
                warnings.warn("LinearSpectrum.convert_x(): new unit ({:s}) is not supported".format(new_unit))
                x_unit = old_unit
                new_x = x
                
        else:
            warnings.warn("LinearSpectrum.convert_x(): old unit ({:s}) is not supported".format(old_unit))
            x_unit = old_unit
            new_x = x
                
        return new_x, x_unit


            
    def convert_y(self, new_unit, y = None, old_unit = ""):
        """
        Convert the y axis from one unit to another. Supported options are absoption, transmission (0 to 1), and transmission (0% to 100%). If the old and new unit are the same, or if the new unit is unsupported, then the output will be the same as the input.
        
        self.y will be used, unless y is given in the parameters. self.y and self.y_unit will not be changed. 
        
        Arguments
        ---------
        new_unit : string
            the unit to convert to. 
        y : ndarray, optional
            If given, this array will be converted. Otherwise self.y will be converted.
        old_unit : string (default: "")
            If given, use this as the current unit. Otherwise, self.y_unit will be used. 
        
        Returns
        -------
        new_y : ndarray
        y_unit : string
    
        """
#         - 2019-01-04/RB: started function
#         - 2019-01-08/RB: y as input, self.y and self.y_unit are not affected. 


        if self.verbose > 1:
            print("LinearSpectrum.convert_y()") 
            
        if old_unit == "":
            if self.y_unit == "":
                warnings.warn("LinearSpectrum.convert_y(): no old unit given")
                return None, old_unit
            else:
                old_unit = self.y_unit
        
        if self.y is None and y is None:
            warnings.warn("LinearSpectrum.convert_y(): y is not given and can't be converted.")
            return None, old_unit
        elif y is None:
            y = self.y[:]


        
        if old_unit in self.absorption_labels:
            if new_unit in self.absorption_labels:
                y_unit = self.absorption_labels[0]
                new_y = y        
            if new_unit in self.transmission_1_labels:
                y_unit = self.transmission_1_labels[0]
                new_y = 10**(-y)
            elif new_unit in self.transmission_pct_labels:
                y_unit = self.transmission_pct_labels[0]
                new_y = 100 * 10**(-y)         
            else:
                warnings.warn("LinearSpectrum.convert_y(): new unit ({:s}) is not supported".format(new_unit)) 
                y_unit = old_unit
                new_y = y
                
        elif old_unit in self.transmission_1_labels:
            if new_unit in self.absorption_labels:
                y_unit = self.absorption_labels[0]
                new_y = -numpy.log10(y)    
            elif new_unit in self.transmission_1_labels:
                y_unit = self.transmission_1_labels[0]
                new_y = y               
            elif new_unit in self.transmission_pct_labels:
                y_unit = self.transmission_pct_labels[0]
                new_y = y * 100      
            else:
                warnings.warn("LinearSpectrum.convert_y(): new unit ({:s}) is not supported".format(new_unit))       
                y_unit = old_unit
                new_y = y
                
        elif old_unit in self.transmission_pct_labels:
            if new_unit in self.absorption_labels:
                y_unit = self.absorption_labels[0]
                new_y = -numpy.log10(y / 100)              
            elif new_unit in self.transmission_1_labels:
                y_unit = self.transmission_1_labels[0]
                new_y = y / 100
            elif new_unit in self.transmission_pct_labels:
                y_unit = self.transmission_pct_labels[0]
                new_y = y           
            else:
                warnings.warn("LinearSpectrum.convert_y(): new unit ({:s}) is not supported".format(new_unit)) 
                y_unit = old_unit
                new_y = y

        else:
            warnings.warn("LinearSpectrum.convert_y(): old unit ({:s}) is not supported".format(old_unit))
            y_unit = old_unit
            new_y = y
                
        return new_y, y_unit
    
    def labels_y(self, y_unit = None, latex = True):
        """
        Return the label for the y-axis of a plot.
        
        Arguments
        ---------
        y_unit : string, optional 
            If not given, use self.y_unit
        latex : bool (True)
            If True, use LaTex notation.
        Returns
        -------
        y_unit_label : string
            A nicely formatted label for the y-axis
        
       
        """           
#          - 2019-01-07/RB: started function
        
        if self.verbose > 1:
            print("LinearSpectrum.labels_y()") 


        if self.y_unit is None and y_unit is None:
            return None
        elif y_unit is None:
            y_unit = self.y_unit
        
        if y_unit in self.absorption_labels:
            return "Absorption (OD)"
        elif y_unit in self.transmission_1_labels:
            return "Transmission"
        elif y_unit in self.transmission_pct_labels:
            if latex:
                return r"Transmission (\%)"
            else:
                return "Transmission (%)"
        else:
            return y_unit
            
    def labels_x(self, x_unit = None, latex = True):
        """
        Return the label for the x-axis of a plot.
        
        Arguments
        ---------
        x_unit : string, optional
            If not given, use self.x_unit
        latex : bool (True)
            If True, use LaTex notation.
        
        Returns
        -------
        x_unit_label : string
            A nicely formatted label for the x-axis.
        
        """           
#         - 2019-01-07/RB: started function
        
        if self.verbose > 1:
            print("LinearSpectrum.labels_x()") 
        if self.verbose > 2:
            if x_unit is None:
                print("  x_unit: None")
            else:
                print("  x_unit: {:}".format(x_unit))
            if self.x_unit is None:
                print("  self.x_unit: None")
            else:
                print("  self.x_unit: {:}".format(self.x_unit))            
                

        
        if self.x_unit is None and x_unit is None:
            return None
        elif x_unit is None:
            x_unit = self.x_unit
        
        if x_unit in self.nm_labels:
            return "Wavelength (nm)"
        elif x_unit in self.um_labels:
            if latex:
                return r"Wavelength ($\mu$m)"
            else:
                return "Wavelength (micron)"
        elif x_unit in self.cm_labels:
            if latex:
                return r"Energy (cm$^{-1}$)"
            else:
                return "Energy (cm-1)"
        elif x_unit in self.ev_labels:
            return "Energy (eV)"  
        else:
            return x_unit            

            
    def plot_spectrum(self, axi = None, **kwargs):
        """
        Plot a spectrum. By default self.x and self.y are used. 
        
        Arguments
        ---------
        - axi (matplotlib axis): if given, this axis will be used. If not, a new figure will be generated.
        - x, y (opt, ndarray): if given, this x will be used instead of self.x. self.x will not be affected. Note that x and y need to have the same dimensions.
        - x_unit, y_unit (opt, string): if given, this unit will be used. self.x will not be affected.
        - interplay between x and x_unit: 
            - if both are not given: self.x and self.x_unit will be used
            - if x_unit is given: self.x will be converted to this unit. self.x will not be affected.
            - if x is given: self.x_unit will be used, if available.
            - if x and x_unit are given: it is assumed that x is already in x_unit. x will not be converted.
        - kwargs for matplotlib.plot:
            - label
            - color
            - lw (linewidth)
            - ls (linestyle)            
            - marker
            - etc.
        

        """      
#         - 2019-01-07/RB: started function
        
        if self.verbose > 1:
            print("LinearSpectrum.plot_spectrum()")         
        if self.verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))
                
        if "x" in kwargs and "x_unit" in kwargs:
            x = kwargs.pop("x")
            x_unit = kwargs.pop("x_unit")
        elif "x" in kwargs:
            x = kwargs.pop("x")
            x_unit = self.x_unit
        elif "x_unit" in kwargs:
            x, x_unit = self.convert_x(kwargs.pop("x_unit")) 
        else:
            x = self.x
            x_unit = self.x_unit
        x_label = self.labels_x(self.x_unit)

        if "y" in kwargs and "y_unit" in kwargs:
            y = kwargs.pop("y")
            y_unit = kwargs.pop("y_unit")
        elif "y" in kwargs:
            y = kwargs.pop("y")
            y_unit = self.y_unit
        elif "y_unit" in kwargs:
            y, y_unit = self.convert_x(kwargs.pop("y_unit")) 
        else:
            y = self.y
            y_unit = self.y_unit
        y_label = self.labels_y(self.y_unit)        

        if axi is None:
            fig = plt.figure()
            axi = fig.add_subplot(111)
            
        axi.plot(x, y, **kwargs)
        
        if "label" in kwargs:
            axi.legend()
        
        axi.set_xlabel(x_label)
        axi.set_ylabel(y_label)
        
    
    # def calculate_y(self, **kwargs):
        # """
        
        # absorption: assume M-1 cm-1:
            # calculate 
        
        # INPUT:
        # - 
        
        # OUTPUT:
        # - -
        
        # CHANGELOG:
        # 2019-01-07/RB: started function
        # """      
        # if self.verbose > 1:
            # print("LinearSpectrum.calculate_y()")         
        # if self.verbose > 2:
            # print("kwargs:")  
            # for k, v in kwargs.items():
                # print("  {:} : {:}".format(k, v))

        # if self.y_unit in self.transmission_1_units:
    
    def __make_header(self, header, col_names, delimiter):
        """
        Private function to generate the header for save_data.
        
        Arguments
        ---------
        header : str
            Will be printed at the top of the file
        col_names : str
            Will be printed just below the header
        delimiter : str
            The sign between columns
        Notes
        -----
        To call this function externally:
        
        >>> P = LinearSpectrum()
        >>> P._LinearSpectrum__make_header()
        
        
        """
        # 2019-03-28/RB: extracted functionality from save_data
        if header is None:
            header = ""
            
        if col_names is None:
            col_names = []
        
        columnnames = ""
        for i in range(len(col_names)):
            if i > 0:   
                columnnames += delimiter
            if col_names[i] is not None:
                columnnames += col_names[i]

        n_h = len(header)
        n_c = len(columnnames)
        
        if n_h == 0 and n_c == 0:
            header = ""
        elif n_h == 0:
            header = columnnames
        elif n_c == 0:
            pass
        else:
            header = header + "\n" + columnnames    
            
        return header
            
    def save_data(self, path, filename = None, **kwargs):
        """
        Save x and y. 
        
        Arguments
        ---------
        path : pathlib.Path
            Path to where the file should be saved. If filename is given, it will be appended. 
        filename : str or pathlib.Path (opt)
            Name of the file. If given, it will be appended to the path. 
            
        Keyword Arguments
        -----------------
        header : str    
            Will be used at the top of the file.             
        x,y : ndarray (opt)
            If given, this will be used instead of `self.x`/`self.y`. This can be mixed, for example `self.x` and another `y` can be saved, in this case the data has to have the same length. 
        x_unit,y_unit : str (opt)
            If given, this will be used instead of `self.x_unit`/`self.y_unit`.         
        data : ndarray (opt)
            If data is given, this will be used instead of `self.x`, `x`, `self.y`, and `y`. 
        columnnames : array-like with str
            Names for the columns of `data`. Will only be used if `data` is given. `x_unit` and `y_unit` will not be used.

        
        
        Notes
        -----
        For other kwargs, see the documentation of `numpy.savetxt': https://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html
        
        The order is `data` > `x` and/or `y` > `self.x` and/or `self.y`. If none are given, an error will be raised

        

        """
#         - 2019-03-27/RB: started function 

        if self.verbose > 1:
            print("LinearSpectrum.save_data()")         
        if self.verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))
                
        delimiter = kwargs.get("delimiter", ",")
        header = kwargs.get("header", "")
        extension = kwargs.get("extension", None)
        comments = kwargs.get("comments", "#")
                
        data = kwargs.get("data", None)
        if data is None:
            x = kwargs.get("x", self.x)
            y = kwargs.get("y",  self.y)
            
            # numpy.stack raises an error if the sizes are not the same, so we don't need to.
            data = numpy.stack((x, y), axis = 1)            
            
            x_unit = kwargs.get("x_unit", self.x_unit)
            y_unit = kwargs.get("y_unit", self.y_unit)
            
            _col_names = [x_unit, y_unit]
            
        else:   
            _col_names = kwargs.get("columnnames", [])

        header = self.__make_header(header, _col_names, delimiter)
            
        paf = CF.make_path_and_filename(path = path, filename = filename, extension = extension, string_out = False, verbose = self.verbose)
            
        numpy.savetxt(paf, data, delimiter = delimiter, comments = comments, header = header)
        

                
    
    
    
                
                
                
                



                
            
            
if __name__ == '__main__': 
    pass            