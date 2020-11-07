# classifier handler

# https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

class knn_handler():

	def __init__(self):
		self.n_neighbors = 5
