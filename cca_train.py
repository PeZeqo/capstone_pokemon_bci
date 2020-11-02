# import pandas as pd
import numpy as np
from sklearn.cross_decomposition import CCA

class cca_handler():

	def __init__(self):
		self.num_targets = 8
		self.sampling_rate = 128.0
		self.frequencies = [30.0, 20.0, 15.0, 12.0, 8.57, 7.5, 6.67]
		self.ref_signals_1s = self.getReferenceSignals1s() 
		self.prediction = None # target 0 to num_targets-1
		self.input_data_1s = None

	def getReferenceSignals1s(self):
		for freq in self.frequencies:
			self.ref_signals.append(self.generateReferenceSignal(128, freq))


	def generateReferenceSignal(self, samples, target_freq):
		reference_signals = []
		t = np.arange(0, (samples/self.sampling_rate), step=1.0/self.sampling_rate)
		reference_signals.append(np.sin(np.pi*2*target_freq*t))
		reference_signals.append(np.cos(np.pi*2*target_freq*t))
		reference_signals.append(np.sin(np.pi*4*target_freq*t))
		reference_signals.append(np.cos(np.pi*4*target_freq*t))
		reference_signals = np.array(reference_signals)

		return reference_signals


	def findCorr(input_data, target_signal):
		cca = CCA(n_components=1)
		result = np.zeros((target_signal.shape)[0])
		for i in range(0, (target_signal.shape)[0]):
			cca.fit(input_data, np.squeeze(target_signal[i,:,:]).T)
			a, b = cca.transform(input_data, np.squeeze(target_signal[i,:,:]).T)
			corr = np.corrcoef(a[:,0], b[:,0])[0, 1]
			result[i] = corr
		return result

	def predict(self, data):
		# pass in the 1s sample
		self.input_data_1s = data
		corrs = [None] * num_targets
		for i in range(num_targets):
			corrs[i] = findCorr(self.input_data_1s, ref_signals_1s[i])
		self.prediction = np.argmax(corrs)
			

	def getPrediction(self):
		self.predict()
		return self.prediction



