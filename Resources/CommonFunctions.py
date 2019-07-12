import warnings

import numpy



def indices_for_binning(x, new_x):
    """
    Returns an array with length x, containing indices how to map the values in x to new_x. 
    new_x is the center of the bin!
    if x is outside of the bins, the index will be -1.
    
    Arguments
    ---------
    x : ndarray
        the old x-axis
    new_x : ndarray
        the new x-axis, the center of the bins

    
    Returns
    -------
    digitized : ndarray
        an array with length x, containing indices how to map the values in x to new_x.
    
    Notes
    -----
    ::
    
        x = numpy.array([2,3,4,1,6,8])
        new_x = numpy.array([1, 3, 5, 7, 9])
        indices_for_binning(x, new_x)
        >>> [1,1,2,0,3,4]
    
    Tip
    ---
    new_x is the center of each bin, so for `new_x = [1, 3, 5, 7, 9]`, the limits are 0-1.99.., 2-3.99.. etc. x = 1 will be written in bins[1] = 2. digitized does not contain 0, even though this is a valid index of new_x, this is why 1 is subtracted at the end.    
    


    """   

        # Notes
    # -----
    
    # - 2019-02-27/RB: started function
    
    x_r = new_x[1] - new_x[0]
    bins = numpy.concatenate((new_x - x_r/2, numpy.array([new_x[-1] + x_r/2])))
    digitized = numpy.digitize(x, bins, right = False) 
    idx = numpy.where(numpy.logical_or(x < bins[0], x >= bins[-1]))[0]
    digitized[idx] = 0
    
    return digitized - 1





def find_overlap_in_arrays(x_list = None, x1 = None, x2 = None, verbose = 0):
    """
    

    
    Arguments
    ---------
    x_list : a list with arrays
    x1,x2 : ndarray (deprecated)

    Returns
    -------
    start,finish : numbers
        The start and finish for an array. 

    Example
    -------
    For x1 = 3456, and x2 is shown:
    
    ::
    
        x1:    3456
        a:  01          no overlap
        b:    23        return x1_min, x2_max
        c:      45      return x2_min, x2_max
        d:        67    return x2_min, x1_max
        e:          89  no overlap
        f:    234567    return x1_min, x1_max

        
    Notes
    -----
    
    - 2019-01-11/RB: started function, extracted from interpolate_two_datasets
    - 2019-01-11/RB: use numpy.amin and amax instead of comparing the beginning/end of the array.
    """    
    if verbose > 1:
        print("SpectraTools.Resources.CommonFunctions:find_overlap_in_arrays()")

    if x1 is not None and x2 is not None:
        warnings.warn("SpectraTools.Resources.CommonFunctions:find_overlap_in_arrays(): using x1 and x2 is DEPRECATED. Use x_list = [x1, x2] instead", DeprecationWarning)
        x_list = [x1, x2]
    elif x1 is not None or x2 is not None:
        print("SpectraTools.Resources.CommonFunctions:find_overlap_in_arrays(): use x_list, or maybe x1, x2, but not only x1 or x2.")
        return None, None
    
    x_min = numpy.zeros(len(x_list))
    x_max = numpy.zeros(len(x_list))
    for i in range(len(x_list)):
        if type(x_list[i]) not in [range, list, numpy.ndarray]:
            return None, None
        x_min[i] = numpy.nanmin(x_list[i])
        x_max[i] = numpy.nanmax(x_list[i])

    if numpy.nanmax(x_min) > numpy.nanmin(x_max):   
        warnings.warn("SpectraTools.Resources.CommonFunctions:find_overlap_in_arrays(): a part is not overlapping.")
        return None, None
    
    start = numpy.nanmax(x_min)
    finish = numpy.nanmin(x_max)
        
    # x1_min = numpy.nanmin(x1)
    # x2_min = numpy.nanmin(x2)
    # x1_max = numpy.nanmax(x1)
    # x2_max = numpy.nanmax(x2)
    
    # if x1_min > x2_max:
        # return None, None
    # elif x2_min > x1_max:
        # return None, None

    # if x1_min > x2_min:
        # start = x1_min
    # else:
        # start = x2_min

    # if x1_max < x2_max:
        # finish = x1_max
    # else:
        # finish = x2_max      
    
    if verbose:
        print(start, finish)
    
    return start, finish
    
    

    
def get_min_max_x(x, min_x = 1e9, max_x = -1e9, verbose = 0):
    """
    Get the minimum and maximum value of x. By using the output of this function as the input for this function with another dataset, the minimum and maximum wavenumber for a set of data can be found. This can be used to make bins for all data. 
    
    Arguments
    ---------
    x : array-like
        Data for which the minimum and maximum should be determined.
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

    if verbose > 1:
        print("SpectraTools.CommonFunctions.get_min_max_x()")    

    if numpy.amin(x) < min_x:
        min_x = numpy.amin(x)
    if numpy.amax(x) > max_x:
        max_x = numpy.amax(x)   
        
    return min_x, max_x   
    
    

    
def find_indices_for_cropping(x, min_x = None, max_x = None, pad = 5, crop_index = False, verbose = 0):
    """
    Find the indices between min_x and max_x and pad them. min_x and/or max_x has to be given. min_x and max_x can be outside the values of x, but the function returns a warning if no indices are found. 

    x has to ascending or descending. 

    Arguments
    ---------
    x : ndarray
        if x is given, it is used instead of self.x    
    min_x : number, optional 
    max_x : number, optional
    pad : number (5)
        Default: 5
    crop_index : bool (False)
        If True, min_x and max_x are considered as indices. Otherwise, they are considered to be values. 

    Returns
    -------
    idx : ndarray 
        Indices to be used

    Notes
    -----
    ::
    
        x = numpy.arange(10)
        
        find_indices_for_cropping(x, min_x = 3.5, max_x = 6.5, pad = 1)
        >>> [3,4,5,6,7]

        find_indices_for_cropping(x, min_x = 3, max_x = 6, pad = 1)
        >>> [2,3,4,5,6,7]   
        
        find_indices_for_cropping(x, min_x = -1, max_x = 6.5, pad = 1)
        >>> [0,1,2,3,4,5,6,7]

        find_indices_for_cropping(x, min_x = 3.5, max_x = 11, pad = 1)
        >>> [3,4,5,6,7,8,9]      
        
        find_indices_for_cropping(x, min_x = -1, max_x = 11, pad = 1)
        >>> [0,1,2,3,4,5,6,7,8,9]    

        find_indices_for_cropping(x, min_x = None, max_x = 6.5, pad = 1)
        >>> [0,1,2,3,4,5,6,7]          
        
        x = numpy.arange(10)[::-1] # i.e. [9,8,7,...0,]        
        find_indices_for_cropping(x, min_x = 3.5, max_x = 6.5, pad = 1)
        >>> [2,3,4,5,6]        

            
    """
    if verbose > 1:
        print("SpectraTools.Resources.CommonFunctions.find_indices_for_cropping()")        
        
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
        warnings.warn("SpectraTools.Resources.CommonFunctions.find_indices_for_cropping(): array ({:}-{:}) does not contain values in the range {:}-{:}".format(x[0], x[-1], min_x, max_x))
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
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    