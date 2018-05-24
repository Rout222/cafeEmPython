from __future__ import print_function
import cv2
import numpy as np
from glob import glob
import gp
import re
import neurolab as nl
import lib
numATTR = 7
histograma = 0


def intervalo(valor, maxV, minV):
	if(maxV>minV):
		if(valor > maxV):
			return 1
		elif(valor < minV):
			return -1
		else:
			return (((valor-minV)*2)/(maxV-minV))-1	
	else:
		if(valor < maxV):
			return 1
		elif(valor>minV):
			return -1
		else:
			return ((((valor-maxV)*2)/(minV-maxV))-1)*-1	
	return 1

def getValues(image):
	values = [[]]
	values[0].append([round((intervalo(lib.distanciaMaiorDefeito(image),350,1200)),2)])
	values[0].append([round((intervalo(lib.calcAreaPercentage(image,lib.getAreaMinElipse(image)),0.99,0.87)),2)])
	values[0].append([round((intervalo(lib.calcAreaPercentage(image,lib.getAreaMinRec(image)),0.78,0.74)),2)])
	values[0].append([round((intervalo(lib.calcAreaPercentage(image,lib.getAreaMinCircle(image)),0.74,0.38)),2)])
	values[0].append([round((intervalo(lib.getAreaMinElipse(image)/lib.getAreaMinCircle(image),0.74,0.4)),2)])
	values[0].append([round((intervalo(lib.getAreaMinElipse(image)/lib.getAreaMinRec(image),0.78,0.84)),2)])
	values[0].append([round((intervalo(lib.getAreaMinCircle(image)/lib.getAreaMinRec(image),1.06,2.29)),2)])
	value = []
	for x in values[0]:
		value.append(float(x[0]))
	return value
def getImages(paths):
	datas = []
	for x in paths:
		datas.append(getValues(cv2.imread(x)))
	return(datas)

def trainFANN(paths):
	datas = []
	expected = []
	for x in paths:
		expected.append([cases[x.split('\\')[-2]]])
		each = getValues(cv2.imread(x))
		datas.append(each)
	return[datas,expected]

def createFANN(paths,network):
	result = trainFANN(paths)
	vector = []
	for i in range(0,len(result[0][0]) -numATTR):
		vector.append([0,1])
	for i in range(numATTR):
		vector.append([-1,1])
	net = nl.net.newff(vector, [5, 1])
	net.train(np.array(result[0]),np.array(result[1]),epochs = 10000)
	net.save(network)

def predictSingleImage(image, network = "semhistograma.net"):
	net = nl.load(network)
	predict = net.sim(np.array([getValues(image)]))
	return(round(predict[0][0]))