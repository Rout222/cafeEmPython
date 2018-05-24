import classificacao
import lib
import cv2
import debug
from glob import glob
# imagens = glob('./cafe/*.JPG')
imagens = glob('./imagens/naoprocessados/*/*.JPG')
config = open('config-corte.txt', "r").readlines()
cv2.namedWindow('Result',cv2.WINDOW_NORMAL)
cv2.namedWindow('Resultado',cv2.WINDOW_NORMAL)
cv2.namedWindow('Corte',cv2.WINDOW_NORMAL)
cv2.namedWindow('Menor Circulo',cv2.WINDOW_NORMAL)
cv2.namedWindow('Menor Elipse',cv2.WINDOW_NORMAL)
cv2.namedWindow('Menor Retangulo',cv2.WINDOW_NORMAL)
cv2.namedWindow('Defeitos',cv2.WINDOW_NORMAL)
config = config[0] if int(config[0]) else 0
cases = {1.0 : [0,255,0], 0. : [255,0,0], -1.: [0,0,255]}
cont = 1
while ( cont == 1 ):
	for i in imagens:
		imgs = cv2.imread(i)
		r = imgs.copy()
		separado = lib.separar(imgs)
		im = lib.removeMask(imgs)
		_,contours,b = cv2.findContours(separado,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		limit = cv2.getTrackbarPos('limit','Result')
		for cnt in contours:
			if(cv2.contourArea(cnt) > int(config)):
				x,y,w,h = cv2.boundingRect(cnt)
				if(x-10 > 0 and y-10 > 0 and h+10 < r.shape[:2][0] and w+10 < r.shape[:2][1]):
					y -= 10
					x -= 10
					h += 10
					w += 10
				roi=imgs[y:y+h,x:x+w]
				color = cases[classificacao.predictSingleImage(roi)]
				cv2.imshow("Corte", roi.copy())
				cv2.imshow("Menor Circulo", debug.showMinCircle(roi.copy())[0])
				cv2.imshow("Menor Elipse", debug.showMinCircle(roi.copy())[1])
				cv2.imshow("Menor Retangulo", debug.showMinRec(roi.copy()))
				cv2.imshow("Defeitos", debug.show(roi.copy()))
				cv2.drawContours(r, [cnt], -1, color, 2, cv2.LINE_AA)
				cv2.imshow("Resultado", r)
				ch = cv2.waitKey(5)
				if ch == 27:
					cont = 0
					break
				if ch == 13:
					cv2.waitKey(0)
				if ch == 32:
					break
		ch = cv2.waitKey(1000)
		if ch == 27:
			cont = 0
			break
		if ch == 13:
			cv2.waitKey(0)
