from threading import Thread
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
        print(self.ml_model)
        self.daemon = True
        self.start()

    def filter_data(self):
        print('to_df')
        self.convert_to_df()
        print(self.eeg_df.head())
        print('decomp')
        approx, decomp = self.wavelet_dwt()
        print('pca')
        pca_approx = self.pca_and_inverse(approx)
        pca_decomp = self.pca_and_inverse(decomp)
        print('sum')
        total_data = np.concatenate((pca_approx, pca_decomp), axis=1)
        data = self.scale_and_normalize(total_data)
        return self.reformat_data(data)

    def convert_to_df(self):
        cols = ['P7', 'O1', 'O2', 'P8', 'Time']
        self.eeg_df = pd.DataFrame(self.eeg_data, columns=cols)
        keep_cols = ['P7', 'O1', 'O2', 'P8']
        self.eeg_df = self.eeg_df[keep_cols]

    def wavelet_dwt(self):
        return pywt.dwt(self.eeg_df.values, 'db5')

    def pca_and_inverse(self, data):
        pca = PCA(0.90)
        pca.fit(data)
        components = pca.transform(data)
        return pca.inverse_transform(components)

    def scale_and_normalize(self, data):
        for col in range(data.shape[1]):
            data[:, col] = minmax_scale(data[:, col])
        return data

    def reformat_data(self, data):
        data = np.transpose(data)
        data = data.reshape(-1, data.shape[0], data.shape[1])
        return data

    def predict_command(self, data):
        print(self.ml_model)
        print(data.shape)
        try:
            pred = self.ml_model.predict(data)
            print(pred)
            command = np.argmax(pred)
            print(command)
            print("NO ERROR")
            return command
        except:
            print("HELLA STINKY")
        return 0

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


