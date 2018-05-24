import lib
import cv2
import os.path
from glob import glob
imagens = glob('./imagens/naoprocessados/*/*.jpg')
print('Foram detectadas ' + str(len(imagens)) + ' imagens')
idx=0
if(os.path.exists("./imagens/cortados/") and os.path.exists("./imagens/cortados/bons/") and os.path.exists("./imagens/cortados/quebrados/") and os.path.exists("./imagens/cortados/sujeira/")):
	for i in imagens:
		imgs = cv2.imread(i)
		ts = lib.thresholdHSV(imgs)
		im = lib.removeMask(imgs)
		_,contours,hierarchy = cv2.findContours(ts,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		limit = cv2.getTrackbarPos('limit','Result')
		for cnt in contours:
			if(cv2.contourArea(cnt) > 300):
				idx += 1
				x,y,w,h = cv2.boundingRect(cnt)
				roi=imgs[y-10:y+h+10,x-10:x+w+10]
				cv2.imwrite("./imagens/cortados/"+i.split('\\')[-2]+"/"+str(idx) + '.jpg', roi)
		print('Imagem ' + i + ' processada')
print('Total de cafes cortados: ' + str(idx)) 