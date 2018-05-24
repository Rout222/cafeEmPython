# import the necessary packages
from __future__ import print_function
import cv2
# from matplotlib import pyplot as plt
import imutils
import numpy as np
#from scipy import signal
from glob import glob
import gp
import re
import neurolab as nl
numATTR = 7
histograma = 0
config = (open("config-hsv.txt", 'r').readlines())
cases = {'quebrados' : 0, 'bons' : 1, 'sujeira' : -1}
def thresholdHSV(image):
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	lower_hsv = np.array([int(config[0]),int(config[1]),int(config[2])])
	upper_hsv = np.array([int(config[3]),int(config[4]),int(config[5])])
	mask = cv2.inRange(hsv,lower_hsv, upper_hsv)
	mask = 255 - mask
	return(mask)

def removeBackGround(image):
	mask = thresholdHSV(image)
	return cv2.bitwise_and(image,image, mask = mask)

def getHistogramsHSV(image):
	image = cv2.cvtColor(removeBackGround(image), cv2.COLOR_BGR2HSV)
	colors = ['h','s','v']
	hist = {}
	for n,x in enumerate(colors):
		hist[x] = cv2.calcHist([image],[n],None,[256],[3,256])
	return hist	
def showMinRec(image):
	thresh = thresholdHSV(image)
	x, contours,hierarchy = cv2.findContours(thresh,2,1)
	bx = 0
	for n,x in enumerate(contours):
		bx = n if cv2.contourArea(x) > cv2.contourArea(contours[bx]) else bx
	cnt = contours[bx]
	rect = cv2.minAreaRect(cnt)
	box = cv2.boxPoints(rect)
	box = np.int0(box)
	cv2.drawContours(image,[box],0,(0,0,255),2)
	return image

def getAreaMinRec(image):
	thresh = thresholdHSV(image)
	x, contours,hierarchy = cv2.findContours(thresh,2,1)
	bx = 0
	for n,x in enumerate(contours):
		bx = n if cv2.contourArea(x) > cv2.contourArea(contours[bx]) else bx
	cnt = contours[bx]
	rect = cv2.minAreaRect(cnt)
	box = cv2.boxPoints(rect)
	box = np.int0(box)
	return(cv2.contourArea(box))
def getAreaMinElipse(image):
	thresh = thresholdHSV(image)
	x, contours,hierarchy = cv2.findContours(thresh,2,1)
	bx = 0
	for n,x in enumerate(contours):
		bx = n if cv2.contourArea(x) > cv2.contourArea(contours[bx]) else bx
	cnt = contours[bx]
	ellipse = cv2.fitEllipse(cnt)
	return((ellipse[1][0]/2)*(ellipse[1][1]/2)*np.pi)

def showMinCircle(image):
	thresh = thresholdHSV(image)
	x, contours,hierarchy = cv2.findContours(thresh,2,1)
	bx = 0
	for n,x in enumerate(contours):
		bx = n if cv2.contourArea(x) > cv2.contourArea(contours[bx]) else bx
	cnt = contours[bx]
	c, r = cv2.minEnclosingCircle(cnt)
	circle = image.copy()
	elipse = image.copy()
	cv2.circle(circle,(int(c[0]), int(c[1])),int(r),(0,0,250),-1)
	ellipse = cv2.fitEllipse(cnt)
	cv2.ellipse(elipse,ellipse,(0,255,0),2)
	return [circle,elipse]

def getAreaMinCircle(image):
	thresh = thresholdHSV(image)
	x, contours,hierarchy = cv2.findContours(thresh,2,1)
	bx = 0
	for n,x in enumerate(contours):
		bx = n if cv2.contourArea(x) > cv2.contourArea(contours[bx]) else bx
	cnt = contours[bx]
	c, r = cv2.minEnclosingCircle(cnt)
	return(np.pi*r*r)
def calcAreaPercentage(image,total =1):
	img = image
	image = removeBackGround(image)
	_, contours, hier= cv2.findContours(thresholdHSV(image), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	bx = 0
	for n,x in enumerate(contours):
		bx = n if cv2.contourArea(x) > cv2.contourArea(contours[bx]) else bx
	area = cv2.contourArea(contours[bx])
	return (area/total)
def getHistogramPeak(histograms):
	dictionary = {}
	for color in histograms:
		xm = 0
		ym = 0
		for y,x in enumerate(histograms[color]):
			if(x > xm):
				xm = x
				ym = y
		dictionary[color] = ym
	return dictionary

def show(image):
	thresh = thresholdHSV(removeBackGround(image))
	_, contours,hierarchy = cv2.findContours(thresh,2,1)
	bx = 0
	for n,x in enumerate(contours):
		bx = n if cv2.contourArea(x) > cv2.contourArea(contours[bx]) else bx
	cnt = contours[bx]

	hull = cv2.convexHull(cnt,returnPoints = False)
	defects = cv2.convexityDefects(cnt,hull)

	for i in range(defects.shape[0]):
	    s,e,f,d = defects[i,0]
	    start = tuple(cnt[s][0])
	    end = tuple(cnt[e][0])
	    far = tuple(cnt[f][0])
	    cv2.line(image,start,end,[0,255,0],2)
	    cv2.circle(image,far,5,[0,0,255],-1)
	return image
def distanciaMaiorDefeito(image):
	thresh = thresholdHSV(image)
	_, contours,hierarchy = cv2.findContours(thresh,2,1)
	bx = 0
	for n,x in enumerate(contours):
		bx = n if cv2.contourArea(x) > cv2.contourArea(contours[bx]) else bx
	cnt = contours[bx]
	hull = cv2.convexHull(cnt,returnPoints = False)
	defects = cv2.convexityDefects(cnt,hull)
	dm = 0
	for i in range(defects.shape[0]):
		d = defects[i,0][-1]
		dm = d if d > dm else dm
		dm = 0 if i == 0 else dm
	return dm

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
def getHistogramsGray(image):
	img = removeBackGround(image)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	hist = cv2.calcHist([img],[0],None,[256],[2,256])
	return hist/hist.sum()
def getValues(image):
	if(histograma):
		values = []
		values.append(getHistogramsGray(image).tolist())
	else:
		values = [[]]
	values[0].append([round((intervalo(distanciaMaiorDefeito(image),350,1200)),2)])
	values[0].append([round((intervalo(calcAreaPercentage(image,getAreaMinElipse(image)),0.99,0.87)),2)])
	values[0].append([round((intervalo(calcAreaPercentage(image,getAreaMinRec(image)),0.78,0.74)),2)])
	values[0].append([round((intervalo(calcAreaPercentage(image,getAreaMinCircle(image)),0.74,0.38)),2)])
	values[0].append([round((intervalo(getAreaMinElipse(image)/getAreaMinCircle(image),0.74,0.4)),2)])
	values[0].append([round((intervalo(getAreaMinElipse(image)/getAreaMinRec(image),0.78,0.84)),2)])
	values[0].append([round((intervalo(getAreaMinCircle(image)/getAreaMinRec(image),1.06,2.29)),2)])
	#values[0].append([round((intervalo(calcAreaPercentage(image),1,0)),2)])
	value = []
	for x in values[0]:
		value.append(float(x[0]))
	return value
def getImages(paths):
	datas = []
	for x in paths:
		datas.append(getValues(cv2.imread(x)))
	return(datas)
def save(paths, classifiers,method):
	casesSave = {1 : "bom-", 0 : "quebrado-", -1 : "sujeira-"}
	for n,i in enumerate(paths):
		aux = (re.sub(r'\W+', '', i))
		image = cv2.imread(i)
		round2 = round(intervalo(classifiers[n],1,-1))
		cv2.imwrite("./output/"+method+"/"+casesSave[int(round2)] +aux +  ".jpg",image)
def trainGP(paths):
	datas = []
	expected = []
	for x in paths:
		expected.append(cases[x.split('\\')[-2]])
		x = cv2.imread(x)
		each = getValues(x)
		datas.append(each)
	return([datas,expected])
def getReal(paths):
	expected = []
	for x in paths:
		each = []
		expected.append(cases[x.split('\\')[-2]])
	return expected

def magic(paths,method, train, network = ""):
	if(method == "GP"):
		save(paths,gp.classifier(getImages(paths), trainGP(train))[1],method)
	else :
		save(paths,testFANN(paths, network)[1],method)
def debug(real, predict):
	debug = {}
	debug['inteirosCertos'] = 0
	debug['inteirosComoSujeiras'] = 0
	debug['inteirosComoQuebrados'] = 0 
	debug['sujeiraCerta'] = 0
	debug['sujeirasComoInteiros'] = 0
	debug['sujeirasComoQuebrados'] = 0
	debug['quebradosCertos'] = 0 
	debug['quebradosComoInteiros'] = 0 
	debug['quebradosComoSujeiras'] = 0
	debug['errors'] = 0
	debug['total'] = len(real)
	for n,x in enumerate(real):
		# print(x, end=" Predict = ")
		# print(predict[n], end = " Depois do intervalo : ")
		aux = predict[n]
		# print(predict[n], end=" Depois de arrendondar: ")
		aux = round(intervalo(aux,1,-1))
		# print(aux)
		if(x == aux):
			if(x == 1):
				# print(x, end = " predict ")
				# print(aux)
				debug['inteirosCertos'] += 1
			elif(x == 0):
				debug['quebradosCertos'] += 1
			else:
				debug['sujeiraCerta'] += 1
		else:
			debug['errors'] += 1
			if(x == 1):
				if(aux == 0):
					debug['inteirosComoQuebrados'] += 1
				else:
					debug['inteirosComoSujeiras'] += 1
			elif(x == 0):
				if(aux == 1):
					debug['quebradosComoInteiros'] += 1
				else:
					debug['quebradosComoSujeiras'] += 1
			else:
				if(aux == 1):
					debug['sujeirasComoInteiros'] += 1
				else:
					debug['sujeirasComoQuebrados'] += 1
	debug['acertos'] = (1-debug['errors']/n)
	return(debug)

def teste(paths):
	real = []
	for x in paths:
		cases = {'quebrados' : 0, 'bons' : 1, 'sujeira' : -1}
		real.append(cases[x.split('\\')[-2]])
	return ([getImages(paths),real])
def testGP(train,paths):
	predict = gp.classifier(getImages(paths),trainGP(train))
	real = []
	for x in paths:
		cases = {'quebrados' : 0, 'bons' : 1, 'sujeira' : -1}
		real.append(cases[x.split('\\')[-2]])
	print(predict[1])
	print(debug(real,predict[1]))
	return([real,predict])
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
def debugFANN(paths,network):
	fann = testFANN(paths,network)
	print(debug(fann[0],fann[1]))
def testFANN(paths,network):
	net = nl.load(network)
	predict = net.sim(np.array(getImages(paths))).tolist()
	for n,x in enumerate(predict):
		predict[n] = x[0]
	real = getReal(paths)
	return [real,predict]

def predictSingleImage(image, network = "semhistograma.net"):
	net = nl.load(network)
	predict = net.sim(np.array([getValues(image)]))
	return(round(predict[0][0]))