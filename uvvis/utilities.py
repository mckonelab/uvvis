import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def clean_raw(filepath):
    
    ''' take raw uvvis .csv and reformat to pandas dataframe for processing

    Inputs:
    filepath (path): path to .csv containing uvvis spectrometer data

    Outputs:
    data (pd.DataFrame): alternating wavelength and absorbance columns
    '''

    raw_data = pd.read_csv(filepath)
    
    data = raw_data.drop(index = 0)
    
    new_labels = []
    for i in np.arange(int(data.shape[1]/2)):
        new_labels.append('nm' + data.columns[int(2*i)])
        new_labels.append('abs' + data.columns[int(2*i)])
    
    data.columns = new_labels
    
    data = data.astype(float)

    return data

def make_reference(data):
    
    ''' take a reference dataframe produced by clean_raw and return averaged spectrum

    Inputs:
    filepath (path): output from cleanraw, alternating wavelength and absorbance columns

    Outputs:
    reference (np.arrray): first column is wavelength, second column is absorbance
    '''

    wavelength = data.iloc[:, 0]

    counter = 0
    spectrum = np.array([])
    for i in np.arange(int(data.shape[1]/2)):
        spectrum = spectrum + data.iloc[:, int(2*i+1)].to_numpy() if spectrum.size else data.iloc[:, int(2*i+1)].to_numpy()
        counter += 1

    reference = np.array([wavelength, spectrum/counter]).transpose()

    return reference

def refer(data, reference):
    
    ''' take a dataframe produced by clean_raw and subtract a reference spectrum

    Inputs:
    data (pd.DataFrame): output from cleanraw, alternating wavelength and absorbance columns
    reference (pd.Dataframe or np.array or float): the reference spectrum to subtract, a float is a constant background
    
    Outputs:
    referenced (pd.DataFrame): alternating wavelength and absorbance columns, referenced to reference
    '''

    referenced = data.copy()

    for i in np.arange(int(data.shape[1]/2)):
        referenced.iloc[:, int(2*i)] = data.iloc[:, int(2*i)]
        referenced.iloc[:, int(2*i + 1)] = data.iloc[:, int(2*i + 1)] - reference

    return referenced
    
def plot_many(data, main_color):
      
    ''' plot a lot of spectra

    Inputs:
    data (pd.DataFrame): output from cleanraw or refer, alternating wavelength and absorbance columns
    main_color (str): color to plot with
    '''

    colors = np.linspace(0.1, 1.0, int(data.shape[1]/2))

    for i in np.arange(int(data.shape[1]/2)):
        plt.plot(data.iloc[:, int(2*i)], data.iloc[:, int(2*i + 1)],
                 color = main_color, alpha = colors[i])

def eps_fit(data, eps, pathlength):
      
    ''' take a referenced dataframe and fit molar absorption coefficients to find apparent concentrations

    Inputs:
    data (pd.DataFrame): output from refer, alternating wavelength and absorbance columns
    eps (pd.Dataframe): the molar absorption coefficients provided at the identical set of wavelengths contained in data
    pathlength (float): the pathlength of the cell used for measurements

    Outputs:
    concs (np.array): fitted concentrations in mol/L [M]
    '''

    def beer_lambert(_, conc):
        return eps*pathlength*conc

    concs = []
    for i in np.arange(int(data.shape[1]/2)):
        fit = curve_fit(beer_lambert, xdata = [], ydata = data.iloc[:, int(2*i + 1)])[0][0]
        concs.append(fit)

    return np.array(concs)