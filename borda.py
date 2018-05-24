import cv2
import numpy as np
from glob import glob
import lib
def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('Result',cv2.WINDOW_NORMAL)
cv2.namedWindow('Mask',cv2.WINDOW_NORMAL)
# Starting with 100's to prevent error while masking
config = open('config-hsv-borda.txt', "r").readlines()
h,s,v = 100,100,100
# Creating track bar
paths = glob("./cafe/*.JPG")
cv2.createTrackbar('h', 'Result',int(config[0]),179,nothing)
cv2.createTrackbar('s', 'Result',int(config[1]),255,nothing)
cv2.createTrackbar('v', 'Result',int(config[2]),255,nothing)
cv2.createTrackbar('img', 'Result', 0, len(paths)-1,nothing)
cv2.createTrackbar('h1', 'Mask',int(config[3]),179,nothing)
cv2.createTrackbar('s1', 'Mask',int(config[4]),255,nothing)
cv2.createTrackbar('v1', 'Mask',int(config[5]),255,nothing)
while(1):

    # get info from track bar and appy to Result
    h = cv2.getTrackbarPos('h','Result')
    h1 = cv2.getTrackbarPos('h1','Mask')
    s = cv2.getTrackbarPos('s','Result')
    s1 = cv2.getTrackbarPos('s1','Mask')
    v = cv2.getTrackbarPos('v','Result')
    v1 = cv2.getTrackbarPos('v1','Mask')
    img = lib.removeMask(cv2.imread(paths[cv2.getTrackbarPos('img','Result')]))
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([h1,s1,v1])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)
    mask = 255 - mask
    cv2.imshow('Mask', mask)
    Result = cv2.bitwise_and(img,img,mask = mask)
    _, contours, b= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, (0,0,255), 2, cv2.LINE_AA, b)
    cv2.imshow('Result',Result)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        saida = open('config-hsv-borda.txt', "w")
        text = str(h) + '\n' + str(s) + '\n' + str(v) + '\n' + str(h1) + '\n' + str(s1) + '\n' + str(v1)
        saida.write(text)
        saida.close()
        break
    cv2.moments(mask)
    print
cv2.destroyAllWindows()