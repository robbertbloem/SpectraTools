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
import SpectraTools.UnitConversion as UC
import SpectraTools.Resources.CommonFunctions as ST_CF

importlib.reload(CT)
importlib.reload(CF)
importlib.reload(MATH)
importlib.reload(UC)
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

        self.nm_labels = UC.nm_labels #["nm"]
        self.um_labels = UC.um_labels # ["um", "micron"]
        self.cm_labels = UC.cm_labels # ["cm-1", "wavenumber"]
        self.ev_labels = UC.ev_labels # ["ev", "eV"]
            
        self.absorption_labels = UC.absorption_labels # ["A"]
        self.milli_absorption_labels = UC.absorption_labels
        self.transmission_1_labels = UC.transmission_1_labels # ["T1"]
        self.transmission_pct_labels = UC. transmission_pct_labels # ["T100"]            

        
    def object_comparison_tests(self, other_class, label):
        """
        Compare this class with another class and warning for inconsistencies for merging. 
        
        Arguments
        ---------
        other_class : object
            Another class
        label : str
            Function name, will be printed in warnings. 
        
        """
        if self.verbose > 1:
            print("LinearSpectrum.object_comparison_tests()")    
    
        if self.__class__.__name__ != other_class.__class__.__name__:
            raise ValueError("LinearSpectrum.{:}: the two classes are not the same ({:} and {:}).".format(label, self.__class__.__name__, other_class.__class__.__name__))

        if self.y is None or other_class.y is None:
            raise ValueError("PAS.{:}(): A.y and/or B.y are None.".format(label))
            
        if label != "concatenate":
            if numpy.all(self.x == other_class.x) == False:
                raise ValueError("PAS.{:}(): A.x and B.x are not the same.".format(label))
            
        if self.x_unit != other_class.x_unit:
            warnings.warn("LinearSpectrum.{:}(): x_units are not the same (A = '{:}' and B = '{:}'). The unit of A will be used.".format(label, self.x_unit, other_class.x_unit))
        elif self.x_unit == "":
            warnings.warn("LinearSpectrum.{:}(): x_unit is not given.".format(label))
        elif self.y_unit != other_class.y_unit:
            warnings.warn("LinearSpectrum.{:}(): y_units are not the same (A = '{:}' and B = '{:}'). The unit of A will be used.".format(label, self.y_unit, other_class.y_unit))
        elif self.y_unit == "":
            warnings.warn("LinearSpectrum.{:}(): y_unit is not given.".format(label))
        
        
    def __add__(self, new):
        """
        Make a new object C, with A.y and B.y added. Only works if A.x and B.x are **exactly** the same.
        The function checks if the x_unit and y_unit are the same for A and B and throws a warning if they are not. 
        
        Arguments
        ---------
        self : object
        new : object
        
        Returns
        -------
        object
        
        """
        if self.verbose > 1:
            print("LinearSpectrum.__add__()")
        
        self.object_comparison_tests(new, label = "__add__")

        x = self.x
        y = self.y + new.y
        
        return LinearSpectrum(x = x, y = y, x_unit = self.x_unit, y_unit = self.y_unit)

    def __sub__(self, new):
        """
        Make a new object C, with B.y subtracted from B.y. Only works if A.x and B.x are **exactly** the same.
        The function checks if the x_unit and y_unit are the same for A and B and throws a warning if they are not. 
        
        Arguments
        ---------
        self : object
        new : object
        
        Returns
        -------
        object
        
        """   
    
        if self.verbose > 1:
            print("LinearSpectrum.__sub__()")
        self.object_comparison_tests(new, label = "__sub__")

        x = self.x
        y = self.y - new.y
        
        return LinearSpectrum(x = x, y = y, x_unit = self.x_unit, y_unit = self.y_unit)

        
    def __truediv__(self, new):
        """
        Make a new object C, with A.y divided by B.y. Only works if A.x and B.x are **exactly** the same.
        The function checks if the x_unit and y_unit are the same for A and B and throws a warning if they are not. 
        
        Arguments
        ---------
        self : object
        new : object
        
        Returns
        -------
        object
        
        """
    
        if self.verbose > 1:
            print("LinearSpectrum.__truediv__()")    
            
        self.object_comparison_tests(new, label = "__truediv__")

        x = self.x
        y = self.y / new.y
        
        return LinearSpectrum(x = x, y = y, x_unit = self.x_unit, y_unit = self.y_unit)        
        
        
    def concatenate(self, new):
        """
        Make a new object C, with the data from objects A and B concatenated.
        
        """
        if self.verbose > 1:
            print("LinearSpectrum.concatenate()")    
            
        self.object_comparison_tests(new, label = "concatenate")      
            
        x = numpy.concatenate((self.x, new.x))
        y = numpy.concatenate((self.y, new.y))
        
        return LinearSpectrum(x = x, y = y, x_unit = self.x_unit, y_unit = self.y_unit)
        
        
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
        
        Wrapper around SpectraTools.CommonFunctions.get_min_max_x().
        
        Arguments
        ---------
        min_x : float
            Default: 1e9
        max_x : float
            Default: -1e9
        
        Returns
        -------
        min_x,max_x : float
        
        Notes    
        -----
        - 2018-12-12/RB: started function
        - 2019-01-08/RB: moved function to LinearSpectrum
        - 2019-07-12/RB: moved function to CommonFunctions
        """
        if self.verbose > 1:
            print("SpectraTools.LinearSpectrum.get_min_max_x()")    
        
        return ST_CF.get_min_max_x(x = self.x, min_x = min_x, max_x = max_x, verbose = self.verbose)
      


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

        idx = ST_CF.find_indices_for_cropping(x = x, min_x = min_x, max_x = max_x, pad = pad, crop_index = crop_index, verbose = self.verbose)

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

        # if self.verbose > 1:
        print("LinearSpectrum.convert_x(): DEPRECATED") 
            
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
      
        return UC.convert_x(x = x, old_unit = old_unit, new_unit = new_unit, verbose = self.verbose)
        
 


            
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


        # if self.verbose > 1:
        print("LinearSpectrum.convert_y(): DEPRECATED") 
            
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

        return UC.convert_y(y = y, old_unit = old_unit, new_unit = new_unit, verbose = self.verbose)

    
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

        # if self.verbose > 1:
        print("LinearSpectrum.labels_y(): DEPRECATED") 

        if self.y_unit is None and y_unit is None:
            return None
        elif y_unit is None:
            y_unit = self.y_unit
        
        return UC.labels_y(y_unit = y_unit, latex = latex, verbose = self.verbose)
        
        
        # if y_unit in self.absorption_labels:
            # return "Absorption (OD)"
        # elif y_unit in self.milli_absorption_labels:
            # return "Absorption (mOD)"            
        # elif y_unit in self.transmission_1_labels:
            # return "Transmission"
        # elif y_unit in self.transmission_pct_labels:
            # if latex:
                # return r"Transmission (\%)"
            # else:
                # return "Transmission (%)"
        # else:
            # return y_unit
            
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
        
        # if self.verbose > 1:
        print("LinearSpectrum.labels_x(): DEPRECATED") 
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
        
        return UC.labels_x(x_unit, latex = True, verbose = 0)          

            
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
            x, x_unit = UC.convert_x(x = self.x, new_unit = kwargs.pop("x_unit"), old_unit = self.x_unit) 
        else:
            x = self.x
            x_unit = self.x_unit
        x_label = UC.labels_x(self.x_unit)

        if "y" in kwargs and "y_unit" in kwargs:
            y = kwargs.pop("y")
            y_unit = kwargs.pop("y_unit")
        elif "y" in kwargs:
            y = kwargs.pop("y")
            y_unit = self.y_unit
        elif "y_unit" in kwargs:
            y, y_unit = self.convert_y(y = self.y, new_unit = kwargs.pop("y_unit"), old_unit = self.y_unit) 
        else:
            y = self.y
            y_unit = self.y_unit
        y_label = UC.labels_y(self.y_unit)        

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