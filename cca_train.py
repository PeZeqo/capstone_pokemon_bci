from pynput.keyboard import Key, Controller
import pandas as pd
import numpy as np
from sklearn.cross_decomposition import CCA
from joblib import load
from matplotlib import pyplot as plt

from FilterClass import Filter

class cca_handler():

	def __init__(self, plotting=False):
		self.sampling_rate = 128.0
		# frequencies calculated by frames/len(array) as seen in flicker_patterns.txt
		self.frequencies = [32.0, 21.33, 14.22, 42.67, 16.0, 64.0, 25.6, 18.29]
		# prediction should be targets 1 to num_targets, not 0 to num_targets - 1
		# based on command_to_keyboard action
		self.prediction = None 
		self.keyboard = Controller()

		self.ref_signals = [] # list of 4 x 128
		self.getReferenceSignals1s()

		self.cca = CCA(n_components=1)
		self.pca = load('models\pca')
		self.channels = ['P7', 'O1', 'O2', 'P8']

		self.fig = None
		self.ax = None
		self.plotter = None

		self.plotting = plotting
		if self.plotting:
			self.start_plot()

		self.filter_obj = Filter()
		

	def start_plot(self):
		self.fig, self.ax = plt.subplots(figsize=(10 ,5))
		# just use target 0 for this exercise
		# for row in self.ref_signals[0]:
		# 	self.ax.plot(row, alpha=0.3)
		self.fig.show()
		# self.fig.canvas.draw()

	def plot_signals(self, data):
		# plot columns data - data is 128 x 4
		self.ax.cla()
		for col in data.T:
			self.ax.plot(col)
		# plt.pause(0.01)
		self.fig.canvas.draw()


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
			# print('correlation target {} = {}'.format(i, corr))
			result[i] = corr
		return result

	def filter(self, data):
		return self.filter_obj.fir(data)

	def predict(self, data):
		# pass in the 1s sample
		data = self.filter(data)
		corrs = self.findCorr(data, self.ref_signals)
		self.prediction = np.argmax(corrs)
		print("Predicted Target: {}".format(self.prediction))
		if self.plotting:
			self.plot_signals(data)

		self.command_to_keyboard_action(self.prediction + 1)


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



