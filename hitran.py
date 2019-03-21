"""
HITRAN (HIgh-resolution TRANsmission molecular absorption database) is an online compilation of transmission data for 50-or-so gasses. 

The API of HITRAN is rather convoluted. This class is a wrapper around the API. The goal is to simplify the use (by only including the parts we need), to set some defaults that are useful for us (like units), and to bring it in line with the class `LinearSpectrum`.

The API works by downloading data from the server to a local database. In `init` this database is created, or connected to, if it already exists. In `import_data` it is first checked if the data is already locally present, to minimize downloading data over and over again. In `calculate_signal` (named to conform to `LinearSpectrum`) the absorption or transmission is calculated. 




"""




import importlib
import os
import pathlib
import numpy

import hapi

import SpectraTools.LinearSpectrum as LS

importlib.reload(hapi)




class hitran(LS.LinearSpectrum):
    """
    A wrapper class around the HITRAN API (HAPI). 
    
    M and I can be found here: https://hitran.org/lbl/
        
    Attributes
    ----------
    db_path : pathlib.Path
        Path where the local database is stored. 
    tablename : str
        Name to reference the data.
    M : int
        Hitran molecule number
    I : int
        Hitran isotopologue number
    min_x,max_x : number
        Minimum and maximum of the wavenumber axis.        
    x : ndarray
        The x-axis. Set by importing the data. 
    y : ndarray
        The values for x. Set by importing the data. 
    x_unit : str
        The unit of the x-axis. 
    y_unit : str
        The unit of the y-axis.   
        
        
    Notes
    -----
    
    - 2019-03-20/RB: started class        
    
    """


    
    def __init__(self, db_path, tablename, M, I, min_x, max_x, verbose = 0, **kwargs):
        """
        Initialize the Hitran class. 
        
        M and I can be found here: https://hitran.org/lbl/
        
        
        Keyword Arguments
        -----------------
        db_path : pathlib.Path
            Path where the local database is stored. 
        tablename : str
            Name to reference the data.
        M : int
            Hitran molecule number
        I : int
            Hitran isotopologue number
        min_x,max_x : number
            Minimum and maximum of the wavenumber axis.             
            
            
        Notes
        -----
        
        - 2019-03-20/RB: started function        
        
        """
        
        if verbose > 1:
            print("SpectraTools.Hitran.__init__()")           
        
        LS.LinearSpectrum.__init__(self, verbose = verbose, **kwargs)
        
        if verbose > 2:
            print("kwargs:")  
            for k, v in kwargs.items():
                print("  {:} : {:}".format(k, v))
                
        self.db_path = db_path
        
        self.tablename = tablename
        self.M = M
        self.I = I
        self.min_x = min_x
        self.max_x = max_x
        
        hapi.db_begin(str(self.db_path))
        


        
    def import_data(self, reload = False):
        """
        Wrapper around hapi.fetch. 

        Keyword Arguments
        -----------------
        reload : bool (False)
            If True, forces a reload of the data. 
            
        Notes
        -----
        
        - 2019-03-20/RB: started function
        
        """
        if self.verbose > 1:
            print("SpectraTools.Hitran.import_data()")       
        
        if reload:
            if self.verbose > 0:
                print("SpectraTools.Hitran.import_data(): downloading data (reload == True)")        
            hapi.fetch(TableName = self.tablename, M = self.M, I = self.I, numin = self.min_x, numax = self.max_x)
        else:
            try:
                nu = hapi.getColumn(self.tablename, 'nu')
                if self.verbose > 1:
                    print(numpy.amin(nu), numpy.amax(nu))
                if numpy.amin(nu) <= self.min_x or numpy.amax(nu) >= self.max_x:    
                    if self.verbose > 0:
                        print("SpectraTools.Hitran.import_data(): downloading data (new range)")
                    hapi.fetch(TableName = self.tablename, M = self.M, I = self.I, numin = self.min_x, numax = self.max_x)
                else:
                    if self.verbose > 0:
                        print("SpectraTools.Hitran.import_data(): no need to download data")               
                        
            except KeyError:
                if self.verbose > 0:
                    print("SpectraTools.Hitran.import_data(): downloading data (new data)")
                hapi.fetch(TableName = self.tablename, M = self.M, I = self.I, numin = self.min_x, numax = self.max_x)
        
        
        
    def remove_data(self, remove_without_confirmation = False):
        """
        Wrapper around hapi.dropTable. Mainly intended for testing. 

        Keyword Arguments
        -----------------
        remove_without_confirmation : bool (False)
            If True, no confirmation will be asked. 
        
        
        Notes
        -----
        
        - 2019-03-20/RB: started function
        
        """
        if self.verbose > 0:
            print("SpectraTools.Hitran.remove_data()")           
        
        if not remove_without_confirmation:
            answer = input("Do you want to delete {:}? yes/no [no] ".format(self.tablename))
            print(answer)
            if answer != "yes":
                print("Removal of data was canceled by the user")
                return 0

        hapi.dropTable(self.tablename)
        
        filepath = self.db_path.joinpath(pathlib.Path("{:s}.data".format(self.tablename)))
        if filepath.is_file():
            os.remove(filepath)

        filepath = self.db_path.joinpath(pathlib.Path("{:s}.header".format(self.tablename)))
        if filepath.is_file():
            os.remove(filepath)        
        

    def calculate_signal(self, environment = {}, line_profile = "default", **kwargs):
        """
        Calculate the spectra.  

        Keyword Arguments
        -----------------
        environment : dict
            Environment variables: `T` for temperature in Kelvin (default: 296), `p` for pressure in atmosphere (default: 1) and `l` for pathlength in centimeters (default is 1). 
        line_profile : str {'default', 'HT', 'Voigt', 'Lorentz', 'Doppler'}
            Default is 'HT'.
        
        For kwargs, see HITRAN API. Not included are: 'SourceTables', 'HITRAN_units', and 'Environment' (for the absorption coefficient calculation) and 'Omegas', 'AbsorptionCoefficient', and 'Environment' (for the spectrum). Instead of 'File', use File_coeff to save the absorption coefficients, and 'File_spectrum' to save the spectrum. 
        
        
        Notes
        -----
        
        - 2019-03-20/RB: started function
        
        """    
        
        if "T" not in environment:
            environment["T"] = 296
        if "p" not in environment:
            environment["p"] = 1
        if "l" not in environment:
            environment["l"] = 1
            
        coeff_kwargs = {}
        abs_trans_kwargs = {}
        
        for k, v in kwargs.items():
            if k in ["Components", "SourceTables", "partitionFunction", "OmegaRange", "OmegaStep", "OmegaWing", "IntensityThreshold", "OmegaWingHW", "GammaL", "LineShift", "Format", "OmegaGrid", "WavenumberRange", "WavenumberStep", "WavenumberWing", "WavenumberWingHW", "WavenumberGrid", "Diluent", "EnvDependences"]:
                coeff_kwargs[k] = v
            
            if k == "File_coeff":
                coeff_kwargs["File"] = v
        
            if k in ["Format", "Wavenumber"]:
                abs_trans_kwargs[k] = v
            
            if k == "File_spectrum":
                abs_trans_kwargs["File"] = v

                
        if line_profile in ['Voigt']:
            w, c = hapi.absorptionCoefficient_Voigt(SourceTables = self.tablename, HITRAN_units = False, Environment = environment, **coeff_kwargs)
        elif line_profile in ['Lorentz']:
            w, c = hapi.absorptionCoefficient_Lorentz(SourceTables = self.tablename, HITRAN_units = False, Environment = environment, **coeff_kwargs)
        elif line_profile in ['Doppler']:
            w, c = hapi.absorptionCoefficient_Doppler(SourceTables = self.tablename, HITRAN_units = False, Environment = environment, **coeff_kwargs)
        elif line_profile in ['default', 'HT']:
            w, c = hapi.absorptionCoefficient_HT(SourceTables = self.tablename, HITRAN_units = False, Environment = environment, **coeff_kwargs)            
        else:
            raise ValueError("'{:}' is not a valid line_profile".format(line_profile))
            
        
        if self.y_unit == "":
            self.x, self.y = hapi.absorptionSpectrum(w, c, Environment = environment)   
            self.y_unit = self.absorption_labels[0]
        if self.y_unit in self.transmission_1_labels:
            self.x, self.y = hapi.transmittanceSpectrum(w, c, Environment = environment)
        elif self.y_unit in self.transmission_pct_labels:
            self.x, self.y = 100 * hapi.transmittanceSpectrum(w, c, Environment = environment)            
        elif self.y_unit in self.absorption_labels:
            self.x, self.y = hapi.absorptionSpectrum(w, c, Environment = environment)       
        else:
            raise ValueError("'{:}' is not a valid value for y_unit".format(self.y_unit))

            
            

        
        
        
        
        
        
        
        