import cv2
import cv2
import time
import os
import sys
import csv
import imutils
import numpy as np
import datetime
import win32api, win32con
import pyautogui

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(0)

winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
currentworkingdirectory = str(os.getcwd()).replace("\\","\\")

# Read three images first:

frame = cam.read()[1]
gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
gray = cv2.GaussianBlur(gray, (21, 21), 0)
firstFrame = gray

pyautogui.moveTo(1000, 1000)

previous_x = 0
previous_y = 0
ispressed = 0
while True:
    frame = cam.read()[1]
    if firstFrame is None:
        firstFrame = gray
        continue
    
    facepath = r"./handtemplaterighttop.png"
    ispressed = 0
    if os.path.isfile(facepath):
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(facepath,0)
        w, h = template.shape[::-1]
    
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.64
      
        loc = np.where( res >= threshold)
        pt = [(0,0)]
      
        while not zip(*loc[::-1]):
            threshold = threshold - 0.02
            loc = np.where( res >= threshold)
    
        counter = 1
        #print("threshold="+str(threshold))   
        for pt2 in zip(*loc[::-1]):
            if threshold > 0.3:
                #print("reach")
                cv2.rectangle(frame, pt2, (pt2[0] + w, pt2[1] + h), (0,0,255), 2)
                #print("right top mouse over")
                #pyautogui.moveTo(pt2[0], pt2[1])
                if previous_x - pt2[0] > 10 and previous_y - pt2[1] < 10 and ispressed == 0:
                    print("right top pressed")
                    pyautogui.moveTo(pt2[0], pt2[1])
                    ispressed = 1
                previous_x = pt2[0]
                previous_y = pt2[1]

        if frame is not None:
            cv2.imshow( winName, cv2.flip( frame, 1 ))

    key = cv2.waitKey(10)
    if key == 27:
      cv2.destroyWindow(winName)
      break
    