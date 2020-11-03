from pynput.keyboard import Key, Controller
import pandas as pd
import numpy as np
from sklearn.cross_decomposition import CCA

class cca_handler():

	def __init__(self):
		self.num_targets = 8
		self.sampling_rate = 128.0
		# self.frequencies = [30.0, 20.0, 15.0, 12.0, 10.0,   8.57, 7.5, 6.67]
		# frequencies calculated by frames/len(array) as seen in flicker_patterns.txt
		self.frequencies = [32.0, 21.33, 14.22, 42.67, 16.0, 64.0, 25.6, 18.29]
		self.prediction = None # target 0 to num_targets-1
		self.keyboard = Controller()

		self.ref_signals = []
		self.getReferenceSignals1s()

		self.cca = CCA(n_components=1)


	def getReferenceSignals1s(self):
		# assume 128 samples 
		for freq in self.frequencies:
			self.ref_signals.append(self.generateReferenceSignal(128, freq))
		self.ref_signals = np.asarray(self.ref_signals)


	def generateReferenceSignal(self, samples, target_freq):
		# get references for one frequency
		reference_signals = []
		t = np.arange(0, (samples/self.sampling_rate), step=1.0/self.sampling_rate)
		reference_signals.append(np.sin(np.pi*2*target_freq*t))
		reference_signals.append(np.cos(np.pi*2*target_freq*t))
		reference_signals.append(np.sin(np.pi*4*target_freq*t))
		reference_signals.append(np.cos(np.pi*4*target_freq*t))
		reference_signals = np.asarray(reference_signals)

		return reference_signals


	def findCorr(self, input_data, target_signal):
		result = np.zeros((target_signal.shape)[0])
		for i in range(0, (target_signal.shape)[0]):
			self.cca.fit(input_data, np.squeeze(target_signal[i,:,:]).T)
			a, b = self.cca.transform(input_data, np.squeeze(target_signal[i,:,:]).T)
			corr = np.corrcoef(a[:,0], b[:,0])[0, 1]
			print('correlation target {} = {}'.format(i, corr))
			result[i] = corr
		return result

	def filter(self, data):
		# data shape is 128 x 4
		return data

	def predict(self, data):
		# pass in the 1s sample
		print("Make Prediction")
		data = self.filter(data)
		corrs = self.findCorr(data, self.ref_signals)
		self.prediction = np.argmax(corrs)
		print("Predicted Command: {}".format(self.prediction))
		self.command_to_keyboard_action(self.prediction)


	def press_release(self, key):
		self.keyboard.press(key)
		self.keyboard.release(key)

	def command_to_keyboard_action(self, command):
		# command 0 is no-action
		if command == 0:
			return
		elif command == 1:
			self.press_release('x')
		elif command == 2:
			self.press_release(Key.up)
		elif command == 3:
			self.press_release('z')
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



