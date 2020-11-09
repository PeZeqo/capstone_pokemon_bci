from scipy.signal import kaiserord, lfilter, firwin, freqz, butter, filtfilt, convolve
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

    # ---------------- Fir filters -------------------------#

    def fir(self, data, s_r=128.0, cutoff_hz=20.0, ripple_db=60.0, width=64.0):
        data = self._format_data(data)
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
        columns = data.shape[1]
        for i in range(columns):
            data[:, i] = lfilter(taps, 1.0, data[:, i])

        return data

    def fir_band(self, data, num_taps=400, band_edges=[1.0, 50.0], fs=128.0, offset_mode='zero'):
        data = self._format_data(data)
        filt = firwin(num_taps, band_edges, pass_zero=False, fs=fs)

        columns = data.shape[1]
        for i in range(columns):
            data[:, i] = convolve(data[:, i], filt, mode='same')
        return data

    # ------------------ Butter filter -------------------------#

    def butter_filter(self, data, s_r=128.0, lowcut=1, highcut=50, order=5):
        data = self._format_data(data)
        # ------------------------------------------------
        # Create a butterworth bandpass filter and apply it to data.
        # ------------------------------------------------
        return self.__apply_butterband_filter(data, s_r, lowcut, highcut, order)

    # ------------------- Helper functions ----------------------#

    def _format_data(self, data):
        if isinstance(data, pd.DataFrame):
            return np.asarray(data.values)
        return data

    def __apply_butterband_filter(self, data, s_r, lowcut, highcut, order):
        columns = data.shape[1]
        for i in range(columns):
            data[:, i] = self.__filter_df_col(data, i, s_r, lowcut, highcut, order)
        return data

    def __filter_df_col(self, data, col, s_r, lowcut, highcut, order):
        #fs = 512.0
        #lowcut = 2.0
        #highcut = 35.0

        vals = data[:, col]
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
# fig, ax = plt.subplots(2, figsize=(15, 8))
# ax[0].plot(df['O1'])
# ax[0].set_title("df")
# print("done")
# #pt = FS.butter_filter(df, 512.0, 1.0, 35.0, 3)
# pt = FS.fir(df)
# #print(type(pt))
# #print(pt[:, 0])
# ax[1].plot(pt[6:, 1])
# ax[1].set_title("filtered")
# #ax[1].set_xlim([256, 2934])
# plt.show()