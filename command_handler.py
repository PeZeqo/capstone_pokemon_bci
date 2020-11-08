import pywt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import minmax_scale
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from joblib import load

class command_handler():
    ml_model = None
    pca = None
    controller = None

    def __init__(self, controller):
        self.controller = controller
        self.load_model_from_json()
        self.ml_model.predict(np.ones((1,12,128)))
        self.pca = load('models\pca')

    def load_model_from_json(self):
        with open("models\model.json", 'r') as json_file:
            json_model = json_file.read()
        self.ml_model = tf.keras.models.model_from_json(json_model)
        self.ml_model.load_weights("models\model.h5")

    def filter_data(self, eeg_data):
        eeg_data = eeg_data[:,:-1]
        print(eeg_data[:5,:])
        approx, decomp = self.wavelet_dwt(eeg_data)
        pca_approx = self.pca_and_inverse(approx)
        pca_decomp = self.pca_and_inverse(decomp)
        total_data = np.concatenate((pca_approx, pca_decomp), axis=1)
        data = self.scale_and_normalize(total_data)
        return self.reformat_data(data)

    def wavelet_dwt(self, eeg_data):
        return pywt.dwt(eeg_data, 'db5')

    def pca_and_inverse(self, data):
        self.pca.fit(data)
        components = self.pca.transform(data)
        return self.pca.inverse_transform(components)

    def scale_and_normalize(self, data):
        for col in range(data.shape[1]):
            data[:, col] = minmax_scale(data[:, col])
        return data

    def reformat_data(self, data):
        data = np.transpose(data)
        data = data.reshape(-1, data.shape[0], data.shape[1])
        return data

    def predict_command(self, data):
        pred = self.ml_model.predict(data)
        command = np.argmax(pred)
        return command

    def command_to_keyboard_action(self, command):
        # command 0 is no-action
        if command == 0:
            return
        elif command == 1:
            self.controller.send_command('x')
        elif command == 2:
            self.controller.send_command('up')
        elif command == 3:
            self.controller.send_command('z')
        elif command == 4:
            self.controller.send_command('left')
        elif command == 5:
            self.controller.send_command('right')
        elif command == 6:
            self.controller.send_command('start')
        elif command == 7:
            self.controller.send_command('down')
        elif command == 8:
            self.controller.send_command('select')

    def predict(self, eeg_data):
        # filter data
        print("Filter Data")
        data = self.filter_data(eeg_data)
        # make command prediction
        print("Make Prediction")
        command = self.predict_command(data)
        # map command to a keyboard action
        print("Predicted Command: {}".format(command))
        self.command_to_keyboard_action(command)
