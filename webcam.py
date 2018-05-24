#!/usr/bin/env python

'''
Multithreaded video processing sample.
Usage:
   video_threaded.py {<video device number>|<video file name>}

   Shows how python threading capabilities can be used
   to organize parallel captured frame processing pipeline
   for smoother playback.

Keyboard shortcuts:

   ESC - exit
   space - switch between multi and single threaded processing
'''

# Python 2/3 compatibility
from __future__ import print_function
import numpy as np
import cv2
import lib
from multiprocessing.pool import ThreadPool
from collections import deque

from common import clock, draw_str, StatValue
import video

if __name__ == '__main__':
    import sys

    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0
    #cap = video.create_capture(fn)
    cap = cv2.VideoCapture('http://192.168.1.103:8080/videofeed')


    def nothing(x):
        pass
    def process_frame(frame, t0):
        imgs = frame
        ts = lib.thresholdHSV(imgs)
        im = lib.removeMask(imgs)
        _,contours,hierarchy = cv2.findContours(ts,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        limit = cv2.getTrackbarPos('limit','input')
        for cnt in contours:
            if(cv2.contourArea(cnt) > cv2.getTrackbarPos('limit','input')):
            #idx += 1
                x,y,w,h = cv2.boundingRect(cnt)
                roi=im[y-10:y+h+10,x-10:x+w+10]
            #cv2.imwrite(str(idx) + '.jpg', roi)
                cv2.rectangle(imgs,(x-10,y-10),(x+w+10,y+h+10),(200,0,0),2)
        return imgs, t0

    threadn = cv2.getNumberOfCPUs()
    pool = ThreadPool(processes = threadn)
    pending = deque()

    threaded_mode = True

    latency = StatValue()
    frame_interval = StatValue()
    last_frame_time = clock()
    cv2.imshow('input', True)
    config = open('config-hsv.txt', "r").readlines()
    cv2.createTrackbar('limit', 'input',int(config[0]),500,nothing)
    cv2.createTrackbar('h', 'input',int(config[0]),179,nothing)
    cv2.createTrackbar('s', 'input',int(config[1]),255,nothing)
    cv2.createTrackbar('v', 'input',int(config[2]),255,nothing)
    cv2.createTrackbar('h1', 'input',int(config[3]),179,nothing)
    cv2.createTrackbar('s1', 'input',int(config[4]),255,nothing)
    cv2.createTrackbar('v1', 'input',int(config[5]),255,nothing)
    while True:
        while len(pending) > 0 and pending[0].ready():
            res, t0 = pending.popleft().get()
            latency.update(clock() - t0)
            draw_str(res, (20, 20), "threaded      :  " + str(threaded_mode))
            draw_str(res, (20, 40), "latency        :  %.1f ms" % (latency.value*1000))
            draw_str(res, (20, 60), "frame interval :  %.1f ms" % (frame_interval.value*1000))
            cv2.imshow('input', res)
        if len(pending) < threadn:
            ret, frame = cap.read()
            t = clock()
            frame_interval.update(t - last_frame_time)
            last_frame_time = t
            task = pool.apply_async(process_frame, (frame.copy(), t))
            pending.append(task)
        ch = 0xFF & cv2.waitKey(1)
        if ch == ord(' '):
            threaded_mode = not threaded_mode
        if ch == 27:
            break
cv2.destroyAllWindows()
