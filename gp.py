import numpy as np
from scipy import stats
from sklearn.gaussian_process import GaussianProcess
# from matplotlib import pyplot as pl
# from matplotlib import cm
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.gaussian_process import GaussianProcess
import cv2
# Standard normal distribution functions
phi = stats.distributions.norm().pdf
PHI = stats.distributions.norm().cdf
PHIinv = stats.distributions.norm().ppf
def ordered_set(in_list,indexs):
	out_list = []
	removed_index = []
	added = []
	for n,val in enumerate(in_list):
		if not val in added:
			out_list.append(val)
			added.append(val)
		else:
			removed_index.append(n)
	removed_index.sort()
	removed_index.reverse()
	for y in removed_index:
		indexs.pop(y)
def classifier(TESTINPUTS, train):
	#ordered_set(train[0],train[1])
	# Design of experiments
	xTrain = np.array(train[0])
	print(xTrain)
	# Observations
	yTrain = (train[1])
	print(yTrain)
	# Instanciate and fit Gaussian Process Model
	gp = GaussianProcess(theta0=1e-3)

	# Don't perform MLE or you'll get a perfect prediction for this simple example!
	gp.fit(xTrain, yTrain)
	y_pred = gp.predict(TESTINPUTS)
	around = []
	for x in y_pred:
		around.append(round(x,0))
	return [y_pred,around]
