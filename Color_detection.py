# & "c:/Users/sayyi/OneDrive/Dokumen/Python Scripts/.mv/Scripts/Activate.ps1"

from __future__ import print_function
from __future__ import division
import cv2
import numpy as np
import argparse
from math import atan2, cos, sin, sqrt, pi

cap = cv2.VideoCapture(0)

#trackbar callback fucntion to update HSV value
def trackbar():
    global H_low,H_high,S_low,S_high,V_low,V_high
    H_low = cv2.getTrackbarPos('low H','controls')
    H_high = cv2.getTrackbarPos('high H','controls')
    S_low = cv2.getTrackbarPos('low S','controls')
    S_high = cv2.getTrackbarPos('high S','controls')
    V_low = cv2.getTrackbarPos('low V','controls')
    V_high = cv2.getTrackbarPos('high V','controls')

def empty(a):
    pass

def momen():
    M = cv2.moments(c)                                                          #menghitung nilai momen pada contour
    cx = int(M['m10']/M['m00'])                                                 #menghitung nilai koordinat x berdasarkan momen
    cy = int(M['m01']/M['m00'])                                                 #menghitung nilai koordinat y berdasarkan momen
    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), 1)                              #menggambar lingkaran pada titik koordinat kontur dengan jari jari 5


#create a seperate window named 'controls' for trackbar
cv2.namedWindow('controls',2)
cv2.resizeWindow("controls", 250,10);


#global variable
H_low = 0
H_high = 179
S_low= 0
S_high = 255
V_low= 0
V_high = 255

#create trackbars for high,low H,S,V 
cv2.createTrackbar('low H','controls',0,179,empty)
cv2.createTrackbar('high H','controls',179,179,empty)

cv2.createTrackbar('low S','controls',0,255,empty)
cv2.createTrackbar('high S','controls',255,255,empty)

cv2.createTrackbar('low V','controls',0,255,empty)
cv2.createTrackbar('high V','controls',255,255,empty)

while(1):

    _, frame = cap.read()                   

    scale_percent = 30 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)             

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)         

    trackbar()

    lower_blue = np.array([H_low,S_low,V_low])           
    upper_blue = np.array([H_high,S_high,V_high])        

    mask = cv2.inRange(hsv, lower_blue, upper_blue)      
    res = cv2.bitwise_and(frame,frame, mask= mask)      

    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)      
    for i, c in enumerate(contours):                                                
        area = cv2.contourArea(c)                                                   
        if area < 1e2 or 1e5 < area:                                                
            continue
        cv2.drawContours(frame, contours, i, (0, 0, 255), 2)       

        momen()                 

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #cv2.imshow('hsv',hsv)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()