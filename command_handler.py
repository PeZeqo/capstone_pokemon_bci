from threading import Thread
import random
from time import sleep
from pynput.keyboard import Key, Controller
import pywt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import minmax_scale

class command_handler(Thread):
    eeg_data = None
    eeg_df = None
    ml_model = None
    keyboard = Controller()

    def __init__(self, eeg_data, ml_model):
        Thread.__init__(self)
        self.eeg_data = eeg_data
        self.ml_model = ml_model
        self.daemon = True
        self.start()

    def filter_data(self):
        self.convert_to_df()
        approx, decomp = self.wavelet_dwt()
        pca_approx = self.pca_and_inverse(approx)
        pca_decomp = self.pca_and_inverse(decomp)
        total_data = np.concatenate((pca_approx, pca_decomp), axis=1)
        return self.scale_and_normalize(total_data)

    def convert_to_df(self):
        sensor_vals = np.delete(self.eeg_data, -1, axis=1)
        cols = ['P7', 'O1', 'O2', 'P8']
        self.eeg_df = pd.DataFrame(sensor_vals, columns=cols)

    def wavelet_dwt(self):
        return pywt.dwt(self.eeg_df.values, 'db5')

    def pca_and_inverse(self, data):
        pca = PCA(0.90).fit(data)
        components = pca.transform(data)
        return pca.inverse_transform(components)

    def scale_and_normalize(self, data):
        for col in range(data.shape[1]):
            data[:, col] = minmax_scale(data[:, col])
        return data

    def predict_command(self, data):
        return self.ml_model.predict(self.eeg_data)

    def press_release(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)

    def command_to_keyboard_action(self, command):
        # command 0 is no-action
        if command == 0:
            return
        elif command == 1:
            self.press_release('z')
        elif command == 2:
            self.press_release(Key.up)
        elif command == 3:
            self.press_release('x')
        elif command == 4:
            self.press_release(Key.left)
        elif command == 5:
            self.press_release(Key.right)
        elif command == 6:
            self.press_release(Key.enter)
        elif command == 7:
            self.press_release(Key.down)
        elif command == 8:
            self.press_release(Key.shift_r)

    def run(self):
        print("Starting thread")

        print("Filter Data")
        data = self.filter_data()

        print("Make Prediction")
        command = self.predict_command(data)

        print("PRESSING: {}".format(command))
        self.command_to_keyboard_action(command)

        print("Ending thread")


