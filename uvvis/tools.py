import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def clean_raw(filepath):

    raw_data = pd.read_csv(filepath)
    
    data = raw_data.drop(index = 0)
    
    new_labels = []
    for i in np.arange(int(data.shape[1]/2)):
        new_labels.append('nm' + data.columns[int(2*i)])
        new_labels.append('abs' + data.columns[int(2*i)])
    
    data.columns = new_labels
    
    data = data.astype(float)

    return data

def plot_many(data, reference, main_color):
    
    colors = np.linspace(0.1, 1.0, int(data.shape[1]/2))

    for i in np.arange(int(data.shape[1]/2)):
        plt.plot(data.iloc[:, int(2*i)], data.iloc[:, int(2*i + 1)] - reference,
                 color = main_color, alpha = colors[i])

    plt.show()

