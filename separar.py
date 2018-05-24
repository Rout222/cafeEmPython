import classificacao
import cv2
import lib
import numpy as np
from glob import glob
def separar(paths):
	for x in paths:
		img = cv2.imread(x)
		img = transformadaDeDistancia(img)
def transformadaDeDistancia(image):
	a, contours, hierarchy = cv2.findContours(lib.thresholdHSV(image),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		#idx += 1
		x,y,w,h = cv2.boundingRect(cnt)
		roi=image[y-10:y+h+10,x-10:x+w+10]
		#cv2.imwrite(str(idx) + '.jpg', roi)
		cv2.rectangle(image,(x-10,y-10),(x+w+10,y+h+10),(200,0,0),2)
	cv2.namedWindow('Result',cv2.WINDOW_NORMAL)
	cv2.imshow('Result',a)
	cv2.waitKey(0)
separar(glob('./cafe/IMG_1764.JPG'))