import cv2
import numpy as np
from FindBalloon import *

def detectHit(img, bboxs):
    img = cropImage(img,0.1)
    img = cv2.resize(img,(0,0),None,0.5,0.5)

    imgBallonList = splitBallons(img, bboxs)
    imgBallonListBalls, directHit = findBallInBallon( imgBallonList)
    showBallon(directHit)
    return directHit

def splitBallons(img, bboxs):
    imgBallonList = []
    for b in bboxs:

        x1, y1, width, height = b[0], b[1], b[2], b[3]
        # Calculate the bottom-right corner coordinates
        x2 = x1 + width
        y2 = y1 + height
        imgBallonList.append(img[y1:y2 , x1:x2])
        
    return imgBallonList

def showBallon(imgBallonList):
    for x, im in enumerate(imgBallonList):
        cv2.imshow(str(x),im)
        
        
def findBallInBallon(imgBallonList):
    imgBallonListBalls = []
    directHit =[]
    for img in imgBallonList:    
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (3, 3), 2, 0)
        
        maxRaduis =50
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 1000, param1=25,param2=30, minRadius=20, maxRadius=maxRaduis)
        if type(circles).__name__ != 'NoneType':
            circles = np.uint16(np.around(circles))
            directHit.append(img)
            for c in circles[0,:]:
                cv2.circle(img, (c[0], c[1]), c[2], (255, 0, 255), 2)
            return imgBallonListBalls, directHit
        imgBallonListBalls.append(img)
    return imgBallonListBalls, directHit