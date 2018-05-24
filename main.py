import cv2
import lib
import gp
import numpy as np
import statistics as s
from matplotlib import pyplot as plt
from glob import glob
train = glob('./cafe2/train/*/*.jpg')
test = glob('./cafe2/processados/*/*.jpg')
# print("---------------------FANN---------------------")
# cafe.createFANN(train,"comhistograma.net")
# cafe.debugFANN(test,"semhistograma.net")
cafe.debugFANN(test,"semhistograma.net")
# print("----------------------GP----------------------")
#aux = cafe.testGP(test,train)

# cafe.magic(test,"FANN", train, "semhistograma.net")

#createFANN(glob('./cafe2/train/*/*.jpg'))
#testFANN(glob('./cafe2/processados/*/*.jpg'))	
#magicGP()
#aux = gp.classifier(cafe.getImages(test),cafe.trainGP(train))
#print(cafe.debug(aux['round'],cafe.getReal2(test)))

# paths = glob("cafe2/processados\\quebrados\\629.jpg")
# bons = [[],[],[],[],[],[]]
# quebrados = [[],[],[],[],[],[]]
# sujeiras = [[],[],[],[],[],[]] 
# for x in paths:#
# 	y = cv2.imread(x)
# 	cafe.show(y)
# 	bons[0].append(cafe.getAreaMinElipse(y)/cafe.getAreaMinCircle(y))#
# 	bons[1].append(cafe.getAreaMinElipse(y)/cafe.getAreaMinRec(y))#
# 	bons[2].append(cafe.getAreaMinCircle(y)/cafe.getAreaMinRec(y))#
# 	bons[3].append(cafe.calcAreaPercentage(y)/cafe.getAreaMinElipse(y))#
# 	bons[4].append(cafe.calcAreaPercentage(y)/cafe.getAreaMinRec(y))#
# 	bons[5].append(cafe.calcAreaPercentage(y)/cafe.getAreaMinCircle(y))#

# for x in test3:#
# 	y = cv2.imread(x)
# 	quebrados[0].append(cafe.getAreaMinElipse(y)/cafe.getAreaMinCircle(y))#
# 	quebrados[1].append(cafe.getAreaMinElipse(y)/cafe.getAreaMinRec(y))#
# 	quebrados[2].append(cafe.getAreaMinCircle(y)/cafe.getAreaMinRec(y))#
# 	quebrados[3].append(cafe.calcAreaPercentage(y)/cafe.getAreaMinElipse(y))#
# 	quebrados[4].append(cafe.calcAreaPercentage(y)/cafe.getAreaMinRec(y))#
# 	quebrados[5].append(cafe.calcAreaPercentage(y)/cafe.getAreaMinCircle(y))#

# for x in test4:#
# 	y = cv2.imread(x)
# 	sujeiras[0].append(cafe.getAreaMinElipse(y)/cafe.getAreaMinCircle(y))#
# 	sujeiras[1].append(cafe.getAreaMinElipse(y)/cafe.getAreaMinRec(y))#
# 	sujeiras[2].append(cafe.getAreaMinCircle(y)/cafe.getAreaMinRec(y))#
# 	sujeiras[3].append(cafe.calcAreaPercentage(y)/cafe.getAreaMinElipse(y))#
# 	sujeiras[4].append(cafe.calcAreaPercentage(y)/cafe.getAreaMinRec(y))#
# 	sujeiras[5].append(cafe.calcAreaPercentage(y)/cafe.getAreaMinCircle(y))#


# print("elipse/circle")
# print(s.mean(bons[0]))
# print(s.mean(quebrados[0]))
# print(s.mean(sujeiras[0]))
# print("elipse/rec")
# print(s.mean(bons[1]))
# print(s.mean(quebrados[1]))
# print(s.mean(sujeiras[1]))
# print("circle/rec")
# print(s.mean(bons[2]))
# print(s.mean(quebrados[2]))
# print(s.mean(sujeiras[2]))
# print("area/elipse")
# print(s.mean(bons[3]))
# print(s.mean(quebrados[3]))
# print(s.mean(sujeiras[3]))
# print("area/rec")
# print(s.mean(bons[4]))
# print(s.mean(quebrados[4]))
# print(s.mean(sujeiras[4]))
# print("area/circle")
# print(s.mean(bons[5]))
# print(s.mean(quebrados[5]))
# print(s.mean(sujeiras[5]))

# cv2.imshow("a",0)
# img = []
# img.append(cv2.imread('./cafe2/processados/bons/10.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/quebrados/1005.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/sujeira/1171.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/bons/1041.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/quebrados/1039.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/sujeira/1161.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/bons/108.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/quebrados/1024.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/sujeira/1136.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/bons/11.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/quebrados/1021.jpg',0).ravel())
# img.append(cv2.imread('./cafe2/processados/sujeira/1160.jpg',0).ravel())
# titles = ['bom','quebrado','sujeira']
# for n,i in enumerate(img):
	# plt.subplot(4,3,n+1),plt.hist(i,256,[0,256])
	# plt.title(titles[n%3])
	# plt.xticks([]),plt.yticks([])
# plt.show()
#print(cafe.getValues(cv2.imread('b.JPG')))