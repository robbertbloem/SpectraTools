r"""
This module contains equations to convert between units. I try to follow the `IUPAC definitions <https://goldbook.iupac.org>`_ as closely as possible.

X-axis: wavelength, wavenumber, ...
-----------------------------------
This is fairly straightforward. 

Absorption and transmission
---------------------------
The basis is the Lambert-Beer law for the **absorbance** :math:`A` is the base-10 logarithm of the ratio of the incident power :math:`P_0` and the radiant power :math:`P`:

.. math:: 
    A &= -\log_{10} \left( \frac{P}{P_0} \right) = \epsilon c l \\
    P &= P_0 10^{-\epsilon c l}
    
where optical path length :math:`l` is in :math:`cm`, the concentration in :math:`c` in :math:`mol \, dm^{-3}`, and the *molar absorption coefficient* :math:`\epsilon` is in :math:`dm^3 \, mol^{-1} \, cm^{-1}`, :math:`M \, cm^{-1}`, or :math:`m^2 \, mol^{-1}` (SI).

The **attenuation coefficient** (formerly called the **extinction coefficient**) is analogous to the absorption coefficient, but includes effects due to scattering and luminescence. The units are the same for the absorption coefficient. 

The **absorbance length** or **attenuation length** is the absorbance or attenuation coefficient for a certain concentration and is in :math:`cm^{-1}`. 

**Transmittance** is the ratio between radiant power :math:`P` and incident power :math:`P_0`:

.. math::
    T = \frac{P}{P_0}

Notes
-----

- 2019-03-04/RB: started module


"""


import numpy
import warnings


nm_labels = ["nm"]
um_labels = ["um", "micron"]
cm_labels = ["cm-1", "wavenumber"]
ev_labels = ["ev", "eV"]
    
absorption_labels = ["A"]
transmission_1_labels = ["T1"]
transmission_pct_labels = ["T100"]            




def prefix_names_to_base10(prefix_name, verbose = 0):  
    """
    Return the base :math:`n` is for :math:`10^n` for standard SI prefixes. Use ``'none'`` for :math:`10^0`. ``None`` is invalid. 
    
    Arguments
    ---------
    prefix_name : str
        SI prefix, such as milli, centi, ...
    
    Returns
    -------
    base : int
        The base of the SI unit.
    
    Notes
    -----

    - 2019-03-04/RB: started function    
    """
    if verbose > 1:
        print("UnitConversion.prefix_names_to_base10()")  
             
    if prefix_name == "yotta":
        return 24
    elif prefix_name == "zetta":
        return 21
    elif prefix_name == "exa":
        return 18
    elif prefix_name == "peta":
        return 15
    elif prefix_name == "tera":
        return 12
    elif prefix_name == "giga":
        return 9
    elif prefix_name == "mega":
        return 6        
    elif prefix_name == "kilo":
        return 3
    elif prefix_name == "hecta":
        return 2
    elif prefix_name == "deca":
        return 1
    elif prefix_name == "none":
        return 0        
    elif prefix_name == "deci":
        return -1
    elif prefix_name == "centi":
        return -2
    elif prefix_name == "milli":
        return -3
    elif prefix_name == "micro":
        return -6
    elif prefix_name == "nano":
        return -9
    elif prefix_name == "pico":
        return -12
    elif prefix_name == "femto":
        return -15
    elif prefix_name == "atto":
        return -18
    elif prefix_name == "zepto":
        return -21
    elif prefix_name == "yocto":
        return -24   
    else:
        warnings.warn("UnitConversion.prefix_names_to_base10(): {:} is an invalid prefix.".format(prefix))
        return None



def base10_to_base10(value, old_base, new_base, power = 1, verbose = 0):
    """
    Convert base 10 to another base 10. The function also accepts standard SI-prefixes. 
    
    Arguments
    ---------
    value : number or array-like
    old_base,new_base : number or string
        Base :math:`n` is for :math:`10^n`. Alternatively, the standard SI-prefixes (milli, centi, etc) can be used, ``'none'`` is for :math:`10^0`. Note: ``None`` is not valid.
    power : number
        For linear (1), square (2), cubic (3). Also valid: -1, -2, etc. Partial powers result in a warning, but not an error. 
      
    Returns
    -------
    new_value : number or array_like
    
    Examples
    --------
    >>> base10_to_base10(1, 'milli', 'micro', 1)
    1e3
    
    >>> base10_to_base10(1, 'milli', 'micro', 3)
    1e9
    
    
    References
    ----------
    A list with SI-prefixes: https://en.wikipedia.org/wiki/Metric_prefix
    
    
    Notes
    -----

    - 2019-03-04/RB: started function    
    
    """
    if verbose > 1:
        print("UnitConversion.base10_to_base10()")           
    
    if old_base is None:
        warnings.warn("UnitConversion.base10_to_base10(): argument old_base is None.")
        return None

    if new_base is None:
        warnings.warn("UnitConversion.base10_to_base10(): argument new_base is None.")
        return None
        
    if type(power) != int:
        warnings.warn("UnitConversion.base10_to_base10(): argument power is not an integer. Continuing.")
    
    if type(old_base) == str:
        old_base = prefix_names_to_base10(old_base)
    if type(new_base) == str:
        new_base = prefix_names_to_base10(new_base)    
     
    old_base = old_base * power
    new_base = new_base * power
    
    return value * 10**old_base / 10**new_base
    
    
    


def convert_x(x, old_unit, new_unit, verbose = 0):
    """
    Convert between x-axis scales. Supported values for units are:
    
    - wavelength (nm): ``nm``
    - wavelength (micron): ``um`` or ``micron``
    - wavenumber: ``cm-1`` or ``wavenumber``
    - electronvolt: ``eV`` or ``ev``
    
    If ``old_unit`` and ``new_unit`` are the same, ``x`` will be returned unchanged as ``new_x``. If either ``old_unit`` or ``new_unit`` are unknown, the function will return ``None, None``.
        
    Arguments
    ---------
    x : number or array_like
    old_unit,new_unit : str
    
    
    Returns
    -------
    new_x : ndarray
    x_unit : string
    
    Notes
    -----

    - 2019-01-04/RB: started function
    - 2019-01-08/RB: x as input, self.x and self.x_unit are not affected. 
    - 2019-03-04/RB: copied to UC from LinearSpectrum, adapted for use outside a class.
    """   
    if verbose > 1:
        print("UnitConversion.convert_x()") 
    
    if old_unit in nm_labels:
        if new_unit in nm_labels:
            x_unit = nm_labels[0]
            new_x = x
        elif new_unit in um_labels:
            x_unit = um_labels[0]
            new_x = x / 1000
        elif new_unit in cm_labels:
            x_unit = cm_labels[0]
            new_x = 1e7 / x    
        elif new_unit in ev_labels:
            x_unit = ev_labels[0]
            new_x = 1239.84 / x
        else:
            warnings.warn("UnitConversion.convert_x(): new unit ({:s}) is not supported".format(new_unit))
            x_unit = None 
            new_x = None
            
    elif old_unit in um_labels:
        if new_unit in nm_labels:
            x_unit = nm_labels[0]
            new_x = x * 1000
        elif new_unit in um_labels:
            x_unit = um_labels[0]
            new_x = x 
        elif new_unit in cm_labels:
            x_unit = cm_labels[0]
            new_x = 1e4 / x    
        elif new_unit in ev_labels:
            x_unit = ev_labels[0]
            new_x = 1.23984 / x
        else:
            warnings.warn("UnitConversion.convert_x(): new unit ({:s}) is not supported".format(new_unit))
            x_unit = None 
            new_x = None
            
    elif old_unit in cm_labels:
        if new_unit in nm_labels:
            x_unit = nm_labels[0]
            new_x = 1e7 / x
        elif new_unit in um_labels:
            x_unit = um_labels[0]
            new_x = 1e4 / x 
        elif new_unit in cm_labels:
            x_unit = cm_labels[0]
            new_x = x    
        elif new_unit in ev_labels:
            x_unit = ev_labels[0]
            new_x = 1239.84 * x / 1e7
        else:
            warnings.warn("UnitConversion.convert_x(): new unit ({:s}) is not supported".format(new_unit))
            x_unit = None 
            new_x = None          
    
    elif old_unit in ev_labels:
        if new_unit in nm_labels:
            x_unit = nm_labels[0]
            new_x = 1239.84 / x
        elif new_unit in um_labels:
            x_unit = um_labels[0]
            new_x = 1.23984 / x
        elif new_unit in cm_labels:
            x_unit = cm_labels[0]
            new_x = 1e7 * x / 1239.84     
        elif new_unit in ev_labels:
            x_unit = ev_labels[0]
            new_x = x
        else:
            warnings.warn("UnitConversion.convert_x(): new unit ({:s}) is not supported".format(new_unit))
            x_unit = None 
            new_x = None
            
    else:
        warnings.warn("UnitConversion.convert_x(): old unit ({:s}) is not supported".format(old_unit))
        x_unit = None 
        new_x = None
            
    return new_x, x_unit


         
def convert_y(y, old_unit, new_unit, verbose = 0):
    """
    Convert the y axis from one unit to another. Supported options are:
    
    - absorbance: ``A``
    - transmission (0 to 1): ``T1``
    - transmission (0% to 100%): ``T100`` 
    
    If ``old_unit`` and ``new_unit`` are the same, ``y`` will be returned unchanged as ``new_y``. If either ``old_unit`` or ``new_unit`` are unknown, the function will return ``None, None``.
        
    Arguments
    ---------
    y : number or array_like
    old_unit,new_unit : str
    

    Returns
    -------
    new_y : ndarray
    y_unit : string
    
    Notes
    -----

    - 2019-01-04/RB: started function
    - 2019-01-08/RB: y as input, y and y_unit are not affected. 
    - 2019-03-04/RB: copied to UC from LinearSpectrum, adapted for use outside a class.    
    """
    if verbose > 1:
        print("UnitConversion.convert_y()")       
        
    if old_unit in absorption_labels:
        if new_unit in absorption_labels:
            y_unit = absorption_labels[0]
            new_y = y        
        if new_unit in transmission_1_labels:
            y_unit = transmission_1_labels[0]
            new_y = 10**(-y)
        elif new_unit in transmission_pct_labels:
            y_unit = transmission_pct_labels[0]
            new_y = 100 * 10**(-y)         
        else:
            warnings.warn("UnitConversion.convert_y(): new unit ({:s}) is not supported".format(new_unit)) 
            y_unit = None
            new_y = None
            
    elif old_unit in transmission_1_labels:
        if new_unit in absorption_labels:
            y_unit = absorption_labels[0]
            new_y = -numpy.log10(y)    
        elif new_unit in transmission_1_labels:
            y_unit = transmission_1_labels[0]
            new_y = y               
        elif new_unit in transmission_pct_labels:
            y_unit = transmission_pct_labels[0]
            new_y = y * 100      
        else:
            warnings.warn("UnitConversion.convert_y(): new unit ({:s}) is not supported".format(new_unit))       
            y_unit = None
            new_y = None

            
    elif old_unit in transmission_pct_labels:
        if new_unit in absorption_labels:
            y_unit = absorption_labels[0]
            new_y = -numpy.log10(y / 100)              
        elif new_unit in transmission_1_labels:
            y_unit = transmission_1_labels[0]
            new_y = y / 100
        elif new_unit in transmission_pct_labels:
            y_unit = transmission_pct_labels[0]
            new_y = y           
        else:
            warnings.warn("UnitConversion.convert_y(): new unit ({:s}) is not supported".format(new_unit)) 
            y_unit = None
            new_y = None


    else:
        warnings.warn("UnitConversion.convert_y(): old unit ({:s}) is not supported".format(old_unit))
        y_unit = None
        new_y = None
            
    return new_y, y_unit
    


# def absorbance_to_molar_absorption_coefficient(A, c, l):
#     """
#     Arguments
#     ---------
#     A : number or ndarray
#         Absorbance
#     c : number
#         concentration
#     l : number
#         path length
#         
#     """
#     return A / (c * l)


# def transmission_for_pathlength(T, new_pathlength, old_pathlength = 1, T_unit = "T1"):
#     """
#     
#     Arguments
#     ---------
#     T : ndarray
#         Transmission 
#     new_pathlength : number
#         The optical path length for the output. 
#     old_pathlength : number (1)
#         The optical path length used for T. 
#     T_unit : str (T1)
#         Transmission for 0-1 ``T1`` or 0-100% ``T100``.
#     
#     Returns
#     -------
#     
#     
#     """
#     pass
    
    
def transmission_to_transmission(T, c, l, c_new, l_new, T_unit = "T1", T_unit_out = None, verbose = 0):
    """
    General function to convert the transmission for certain conditions, to transmission for other conditions. 
    
    
    
    Arguments
    ---------
    T : ndarray
        Transmission
    c : number
        Concentration of T
    l : number
        Optical path length of T
    c_new : number
        Concentration of the output
    l_new : number
        Optical path length of the output.
    T_unit : str (T1)
        Transmission for 0-1 ``T1`` or 0-100% ``T100``.
    T_unit_out : str (None)
        Units of output. If None, the output will be the same as the input.
    
    Returns
    -------
    T_new : ndarray
        The transmission for the new conditions. 
    
        
    Notes
    -----
    2019-03-04/RB: started function    
        
    
    """
    if verbose > 1:
        print("UnitConversion.transmission_to_transmission()")         
    
    if T_unit != "T1":
        T, dump = convert_y(T, T_unit, "T1", verbose = verbose)

    idx = numpy.asarray(numpy.logical_or(T <= 0, T > 1)).nonzero()
    T[idx] = 1
    # idx = numpy.asarray(T > 1).nonzero()
    # T[idx] = 1
    
    ac = -numpy.log10(T) / (c * l)
    
    T_new = 10**(-ac * c_new * l_new)

    T_new[idx] = numpy.nan

    if T_unit_out is None:
        if T_unit != "T1":
            T_new, dump = convert_y(T_new, "T1", T_unit)
    else:   
        T_new, dump = convert_y(T_new, "T1", T_unit_out)

    return T_new
    


if __name__ == "__main__": 
    pass













