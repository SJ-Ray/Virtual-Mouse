# -*- coding: utf-8 -*-
"""
Created on Sun May  6 22:42:14 2018

@author: SURAJ KUMAR
"""

import cv2
import numpy as np
import pyautogui

pyautogui.FAILSAFE=False

cap=cv2.VideoCapture(0)
screen_res=pyautogui.size()

cap.set(3,screen_res[0]/2)
cap.set(4,screen_res[1]/2)
video_res=(cap.get(3),cap.get(4))

rx,ry=(2.8,2.9)

ret=True

posXList=list()
posYList=list()
clickHistory=list()

while ret:
    ret,frame=cap.read()
    flipped=cv2.flip(frame,1)
    hsv_frame=cv2.cvtColor(flipped,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv_frame,np.array([20,130,130]),np.array([30,255,255]))
   
    blurred_mask=cv2.medianBlur(mask,5)
    
    k_dilated=np.ones((5,5),np.uint8)
    dilated_mask=cv2.dilate(blurred_mask,k_dilated,5)
    
    
    con_img,contours,heirarchy=cv2.findContours(dilated_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours)>0:
        M = cv2.moments(contours[0])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        posX=int(cX*rx)
        posY=int(cY*ry)
        
        posXList.append(posX)
        posYList.append(posY)
        
        x_len,y_len=len(posXList),len(posYList)
       
        pyautogui.moveTo(posX,posY, duration=0)
        
        if x_len==8:
            print("X list",posXList)
            print("Y list",posYList)
            xmax=max(set(posXList),key=posXList.count)
            ymax=max(set(posYList),key=posYList.count)
            x_count=posXList.count(xmax)
            y_count=posYList.count(ymax)
            if x_count>2 and y_count>2:
        
                if len(clickHistory)==0:
                    clickHistory.append((xmax,ymax))
                    pyautogui.click(x=xmax, y=ymax)
                else:
                    x,y=clickHistory[0]
                    if (xmax in range(x-10,x+10)) and (ymax in range(y-10,y+10)):
                        pyautogui.moveTo(xmax, ymax)
                        pyautogui.click(clicks=2)
                    clickHistory.clear()
                
            posXList.clear()
            posYList.clear()
        
        
        cv2.circle(flipped, (cX, cY), 7, (0,255, 0), -1)
        cv2.drawContours(flipped,contours, -1, (0, 0, 255), 2)
        
    cv2.imshow("original",flipped)
    
    
    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()