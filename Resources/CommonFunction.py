import numpy



def indices_for_binning(x, new_x):
    """
    Returns an array with length x, containing indices how to bin the values in x to new_x. 
    new_x is the center of the bin!
    
    INPUT:
    - x (ndarray): 
    - new_x (ndarray): 

    
    OUTPUT:
    
    
    CHANGELOG:
    2019-02-27/RB: started function
    """       
    x_r = new_x[1] - new_x[0]
    bins = numpy.concatenate((new_x - x_r/2, numpy.array([new_x[-1] + x_r])))
    digitized = numpy.digitize(x, bins, right = False)
    return digitized    





def find_overlap_in_arrays(x1, x2, verbose = 0):
    """
    
    INPUT:
    - x1 and x2: ndarray. x1 and x2 can contain NaN.

    OUTPUT:
    - 

    LOGIC: 
    
    x1:    3456
    a:  01          no overlap
    b:    23        return x1_min, x2_max
    c:      45      return x2_min, x2_max
    d:        67    return x2_min, x1_max
    e:          89  no overlap
    f:    234567    return x1_min, x1_max
    
    CHANGELOG:
    2019-01-11/RB: started function, extracted from interpolate_two_datasets
    2019-01-11/RB: use numpy.amin and amax instead of comparing the beginning/end of the array.
    """    
    if verbose > 1:
        print("SpectraTools.Resources.CommonFunctions:find_overlap_in_arrays()")
        
    if type(x1) not in [range, list, numpy.ndarray]:
        return None, None
    if type(x2) not in [range, list, numpy.ndarray]:
        return None, None
        
    x1_min = numpy.nanmin(x1)
    x2_min = numpy.nanmin(x2)
    x1_max = numpy.nanmax(x1)
    x2_max = numpy.nanmax(x2)
    
    if x1_min > x2_max:
        return None, None
    elif x2_min > x1_max:
        return None, None

    if x1_min > x2_min:
        start = x1_min
    else:
        start = x2_min

    if x1_max < x2_max:
        finish = x1_max
    else:
        finish = x2_max      
    
    if verbose:
        print(start, finish)
    
    return start, finish