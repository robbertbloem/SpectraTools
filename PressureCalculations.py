"""


"""

import numpy
import warnings

def molar_mass_dry_air():
    """
    Molar mass of dry air. 
    
    Notes
    -----
    https://www.engineeringtoolbox.com/molecular-mass-air-d_679.html
    https://en.wikipedia.org/wiki/Atmosphere_of_Earth
    """
    return 28.9647


def water_vapour_saturation_pressure(T, isCelsius = True):
    """
    Calculate the water vapour saturation pressure above liquid water. This equation is valid between 0 degree C and 374 degree C (the critical temperature). It is valid for low-ish pressures. For pressures above 10 bar or so, an enhancement factor needs to be included. 
    
    Arguments
    ---------
    T : number
        The temperature in Kelvin, unless `isCelsius` is set to True.
    isCelsius : Bool    
        True if the temperature is in Celsius (default), False if it is in Kelvin. 
    
    Notes
    -----
    https://www.vaisala.com/en/system/files?file=documents/Humidity_Conversion_Formulas_B210973EN.pdf page 4
    https://thermophysics.ru/pdf_doc/IAPWS_1995.pdf eq 2.5
    
    """
    if isCelsius:
        T += 273.15

    if T < 273.15: 
        warnings.warn("Temperature {:} K is below freezing. This function is not valid.".format(T))
    elif T > 647.096:
        warnings.warn("Temperature {:} K is above the critical temperature. This function is not valid.".format(T))
    
    Tc = 647.096 # critical temperature, K
    Pc = 22.064e6 # critical pressure Pa
    C1 = -7.85951783
    C2 =  1.84408259
    C3 = -11.7866497
    C4 =  22.6807411
    C5 = -15.9618719
    C6 =  1.80122502
    v = 1 - T / Tc # vartheta = transformed temperature
    
    a = C1 * v + C2 * v**1.5 + C3 * v**3 + C4 * v**3.5 + C5 * v**4 + C6 * v**7.5
    Pws = Pc * numpy.exp(Tc * a / T)
    return Pws
    

def ice_vapour_saturation_pressure(T, isCelsius = True):
    """
    Arguments
    ---------
    T : number
        The temperature in Kelvin, unless `isCelsius` is set to True.
    isCelsius : Bool    
        True if the temperature is in Celsius (default), False if it is in Kelvin. 

    Notes
    -----
    https://www.vaisala.com/en/system/files?file=documents/Humidity_Conversion_Formulas_B210973EN.pdf page 5
    """
    if isCelsius:
        T += 273.15

    if T < 173.15: 
        warnings.warn("Temperature {:} K is below the triple point temperature. This function is not valid.".format(T))
    elif T > 273.15:
        warnings.warn("Temperature {:} K is above freezing. This function is not valid.".format(T))    
    
    Tn = 273.16 # triple point temperature, K
    Pn = 611.657 # vapor pressure at triple point temperature, Pa
    c0 = -13.928169
    c1 =  34.707823    
    
    theta = T / Tn
    Pwi = Pn * numpy.exp(c0 * (1 - theta**-1.5) + c1 * (1 - theta**-1.25))
    return Pwi
    
    
    
    
if __name__ == "__main__": 
    pass