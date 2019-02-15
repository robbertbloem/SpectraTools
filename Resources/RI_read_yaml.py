import importlib
import yaml
import urllib

import numpy
import matplotlib 
import matplotlib.pyplot as plt



import PythonTools.CommonFunctions as CF

importlib.reload(CF)

def string_to_cols(string, ncols = 1, verbose = 0):
    """
    Data is a string. Convert this to a ndarray ncols. 
    """
    if verbose > 1:
        print("RefractiveIndex.Resources.RI_read_yaml.string_to_cols()")       
    data = CF.string_with_numbers_to_list(string)
    if ncols > 1:
        n = int(len(data) / ncols)
        data = numpy.reshape(data, (n, ncols))
    return data   
  
  
def import_refractive_index(paf, verbose = 0):
    
    if verbose > 1:
        print("RefractiveIndex.Resources.RI_read_yaml.import_refractive_data()")   
    
    stream = open(paf, "r")
    docs = yaml.load_all(stream)

    output = {}

    for doc in docs:
        
        if verbose > 2:
            for k,v in doc.items():
                print(k, "->", v)

        if "coefficients" in doc["DATA"][0]:
            output["coefficients"] = string_to_cols( doc["DATA"][0]["coefficients"], ncols = 1, verbose = verbose)
        
        if "type" in doc["DATA"][0]:
            output["type"] = doc["DATA"][0]["type"]
        
        if "data" in doc["DATA"][0]:       
            if output["type"] == "tabulated nk":
                output["data"] = string_to_cols(doc["DATA"][0]["data"], ncols = 3, verbose = verbose)
            elif output["type"] == "tabulated n":            
                output["data"] = string_to_cols(doc["DATA"][0]["data"], ncols = 2, verbose = verbose)
            else:
                print("Unknown data type")
                
        if "range" in doc["DATA"][0]: 
            output["range"] = string_to_cols( doc["DATA"][0]["range"], ncols = 1, verbose = verbose)

        elif "wavelength_range" in doc["DATA"][0]: 
            output["range"] = string_to_cols( doc["DATA"][0]["wavelength_range"], ncols = 1, verbose = verbose)
            
        if "REFERENCES" in doc:
            output["references"] = doc["REFERENCES"]

        if "COMMENTS" in doc:
            output["comments"] = doc["COMMENTS"]
            
        if "INFO" in doc:
            output["info"] = doc["INFO"]

    return output
    




if __name__ == "__main__": 

    pass
