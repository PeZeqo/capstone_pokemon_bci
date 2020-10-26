# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 02:04:58 2020

This program takes streamed in EEG Headset Signal and applies a Principal
Component Analysis (PCA) filter to reduce background noise. In essence, we are
using AI technology to locate the strongest channels in our signal and using
them to reconstruct our signal with less noise.

Generally, preserving less variance (20%) works better than the default option
of 50%

@author: Michael
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

'''Each set of data collected at a given timestamp should be seen as a row in the
pandas dataframe. If for example we know that [45, 50, 1904353455] corresponds
to the O1 and O2 signals at timestamp 1904353455, then row "1904353455" should
have 45 in the O1 column and 50 in the O2 column. Seperate these rows by input channel
and create a pandas dataframe'''
numpy_data = np.array([<Array of O1 Values>, <Array of O2 Values>, etc.])  # each timestamp
df = pd.DataFrame(data=numpy_data, index=["time1", "time2", etc.], columns=["O1", "O2", etc.])


'''Option to read a CSV as input'''
# csv = ("C:/Users/Michael/Downloads/sultan_checkerboard_1.csv")
# # load dataset into Pandas DataFrame
# df = pd.read_csv(csv)
time = df['Timestamp']

# This loop removes columns with "NaN" values. That is to say, the "marker" columns
for c in df.columns:
    col = c.lower()
    if "eeg" not in col:# and "eeg.o" not in col:
        del df[c]
for c in df.columns:
    col = c.lower()
    NonElectrodes = ['counter','interpolated', 'rawcq', 'battery', 'marker']
    for n in NonElectrodes:
        if n in col:
            del df[c]
            break

'''  Optional training method of reconstructing a signal with random
  white Gaussian noise added in. Change values as you see fit! '''

# np.random.seed(42)  
# noisy = np.random.normal(df, 4)

# Create a PCA object of the signal, preserving 0.20 (20%) of the variance.
pca = PCA(0.2).fit(df)  # Feel free to play around with the variance value! 

# pca.n_components = 1  # Hard-code number of principal components to rebuild signal from (not recommended)

from matplotlib import pyplot as plt
plt.plot(time, df['EEG.O1'])  # View original signal of given electrode (blue)

# Undergo PCA analysis of the input signal to determine the strongest sources
components = pca.transform(df)

# Reconstruct original signal from strongest sources, reducing overall noise
filteredSignal = pca.inverse_transform(components)
plt.plot(time, filteredSignal[:,6])  # view filtered signal overlay (orange)
