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
hand_cascade = cv2.CascadeClassifier(r"./hand.xml")
while True:
    frame = cam.read()[1]
    if firstFrame is None:
        firstFrame = gray
        continue
    
    handpath = r"./hand.png"
    ispressed = 0
    if os.path.isfile(handpath):
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hands = hand_cascade.detectMultiScale(img_gray, 1.1, 5)
        
        for (x,y,w,h) in hands:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

        if frame is not None:
            cv2.imshow( winName, cv2.flip( frame, 1 ))

    key = cv2.waitKey(10)
    if key == 27:
      cv2.destroyWindow(winName)
      break
    