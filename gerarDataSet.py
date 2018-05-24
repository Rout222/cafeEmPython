import lib
import cv2
import debug
from glob import glob
import click # gera a progress bar
imagens = glob('./imagens/naoprocessados/*/*.JPG')
config = int(open('config-corte.txt', "r").readlines()[0])
path = {'quebrados' : 1, 'bons' : 0, 'sujeira' : 2}
def getValues(roi):
	values = []
	values.append(lib.distanciaMaiorDefeito  (roi))
	values.append(lib.getAreaMinElipse       (roi))
	values.append(lib.getAreaMinRec          (roi))
	values.append(lib.getAreaMinCircle       (roi))
	values.append(lib.calcAreaPercentage	 (roi))
	return values
cont = 0 
resultado = []
with click.progressbar(imagens, label='Processando imagens') as bar:
	for i in bar:
		classe = path[i.split("\\")[1]] # classe da imagem toda
		imgs = cv2.imread(i)
		r = imgs.copy()
		separado = lib.separar(imgs)
		im = lib.removeMask(imgs)
		_,contours,b = cv2.findContours(separado,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		for cnt in contours:
			if(cv2.contourArea(cnt) > int(config)):
				x,y,w,h = cv2.boundingRect(cnt)
				if(x-10 > 0 and y-10 > 0 and h+10 < r.shape[:2][0] and w+10 < r.shape[:2][1]):
					y -= 10
					x -= 10
					h += 10
					w += 10
				roi=imgs[y:y+h,x:x+w]
				cont +=1
				#resultadoRoi = getValues(roi) + [i.split("\\")[1]]
				resultadoRoi = getValues(roi) + [classe]
				resultado += [resultadoRoi]

import csv
cabecalho = ['convexHull','Elipse','Rec','Circle', 'Area', 'Classe']
with open("output.csv",'w', newline='') as resultFile:
	wr = csv.writer(resultFile, dialect='excel')
	with click.progressbar(resultado, label='Escrevendo arquivo output.csv') as bar:
		wr.writerow(cabecalho)
		for item in bar:
			wr.writerow(item)