from threading import Thread
from pynput.keyboard import Key, Controller
import pywt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import minmax_scale
import tensorflow as tf

class command_predict_thread(Thread):
    eeg_data = None
    ml_model = None
    keyboard = Controller()

    def __init__(self, eeg_data, ml_model):
        Thread.__init__(self)
        self.eeg_data = eeg_data
        print(self.eeg_data)
        self.ml_model = ml_model
        print(self.ml_model)
        print("init pred done")
        self.daemon = True
        self.start()

    def setup(self):
        print(self.ml_model)
        self.ml_model = tf.keras.models.clone_model(self.ml_model)
        print(self.ml_model)
        self.ml_model.predict(np.ones((1,12,128)))
        print("init pred done")

    def filter_data(self):
        print('to_df')
        df = self.convert_to_df()
        print(df.head())
        print('decomp')
        approx, decomp = self.wavelet_dwt(df)
        print('pca')
        pca_approx = self.pca_and_inverse(approx)
        pca_decomp = self.pca_and_inverse(decomp)
        print('sum')
        total_data = np.concatenate((pca_approx, pca_decomp), axis=1)
        data = self.scale_and_normalize(total_data)
        return self.reformat_data(data)

    def convert_to_df(self):
        cols = ['P7', 'O1', 'O2', 'P8', 'Time']
        eeg_df = pd.DataFrame(self.eeg_data, columns=cols)
        keep_cols = ['P7', 'O1', 'O2', 'P8']
        return eeg_df[keep_cols]

    def wavelet_dwt(self, df):
        return pywt.dwt(df.values, 'db5')

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

    def load_model_from_json(self):
        with open("../models/model.json", 'r') as json_file:
            json_model = json_file.read()
        model = tf.keras.models.model_from_json(json_model)
        model.load_weights("models\model.h5")
        return model

    def predict_command(self, data):
        # model = self.load_model_from_json()
        # model.predict(np.ones((1,12,128)))
        try:
            print("make pred")
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

        print("Running Setup")
        self.setup()

        print("Filter Data")
        data = self.filter_data()
        print(data)

        print("Make Prediction")
        command = self.predict_command(data)

        # print("PRESSING: {}".format(command))
        # self.command_to_keyboard_action(command)

        print("Ending thread")


