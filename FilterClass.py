# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from scipy.signal import kaiserord, lfilter, firwin, freqz, butter, filtfilt
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

class Filter:

    # these three functions use a sample rate field but i don't think it makes sense to use
    # leaving it here anyway for now
    def __init__(self, sample_rate=128.0):
        self.__sample_rate = sample_rate

    def get_sample_rate(self):
        return self.__sample_rate

    def set_sample_rate(self, new_rate):
        self.__sample_rate = new_rate

    def fir(self, data, s_r=128.0, cutoff_hz=20.0, ripple_db=60.0, width=64.0):
        #------------------------------------------------
        # Create a FIR filter and apply it to data.
        #------------------------------------------------

        # The Nyquist rate of the signal.

        nyq_rate = s_r / 2.0
        
        # The desired width of the transition from pass to stop,
        # relative to the Nyquist rate.  We'll design the filter
        # with a 60 Hz transition width.
        width = width/nyq_rate
        
        # The desired attenuation in the stop band, in dB.
        #ripple_db = 60.0
        
        # Compute the order and Kaiser parameter for the FIR filter.
        N, beta = kaiserord(ripple_db, width)
        
        # The cutoff frequency of the filter.
        #cutoff_hz = 20.0
        
        # Use firwin with a Kaiser window to create a lowpass FIR filter.
        taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        
        # Use lfilter to filter x with the FIR filter.
        return lfilter(taps, 1.0, data)


    def butter_filter(self, data, s_r=128.0, lowcut=1, highcut=50, order=5):
        print("sample rate inside butter: ", s_r)
        # ------------------------------------------------
        # Create a butterworth bandpass filter and apply it to data.
        # ------------------------------------------------
        return self.__apply_butterband_filter(data, s_r, lowcut, highcut, order)



    def __apply_butterband_filter(self, input_df, s_r, lowcut, highcut, order):
        df = input_df.copy()
        for col in df.columns:
            df[col] = self.__filter_df_col(df, col, s_r, lowcut, highcut, order)

        return df

    def __filter_df_col(self, df, col, s_r, lowcut, highcut, order):
        #fs = 512.0
        #lowcut = 2.0
        #highcut = 35.0

        vals = df[col].values
        return self.__butter_bandpass_filter(vals, lowcut, highcut, s_r, order)

    def __butter_bandpass(self, lowcut, highcut, fs, order):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def __butter_bandpass_filter(self, data, lowcut, highcut, fs, order):
        b, a = self.__butter_bandpass(lowcut, highcut, fs, order=order)
        data = data * 50  # amplify data
        y = filtfilt(b, a, data)
        return y

# some test code just to show it runs (change for ur machine)
# df = pd.read_csv("C:/Users/Chris Zarba/PycharmProjects/capstone_pokemon_bci/recordings/simple_recording_sultan_0.csv")
# FS = Filter()
# print(FS.get_sample_rate())
# print(FS.butter_filter(df))