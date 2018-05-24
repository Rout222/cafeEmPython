import cafe
import cv2
from glob import glob
imagens = glob('./cafe2/naoprocessados/*/*.JPG')
idx=0
for i in imagens:
	imgs = cv2.imread(i)
	ts = cafe.thresholdHSV(imgs)
	im = cafe.removeBackGround(imgs)
	_,contours,hierarchy = cv2.findContours(ts,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	limit = cv2.getTrackbarPos('limit','Result')
	for cnt in contours:
		if(cv2.contourArea(cnt) > 230):
			idx += 1
			x,y,w,h = cv2.boundingRect(cnt)
			roi=imgs[y-10:y+h+10,x-10:x+w+10]
			cv2.imwrite("./cafe2/processados/"+i.split('\\')[-2]+"/"+str(idx) + '.jpg', roi)