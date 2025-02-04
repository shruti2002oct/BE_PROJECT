import cv2
import numpy as np

def findBalloons(img):
    img = cropImage(img,0.1)
    img = preprocess(img)   
    cv2.imshow(" ",img)
    img , bbox = findContours(img)
    return img , bbox

def cropImage(img,cropVal):
    h,w,c = img.shape
    img = img[int(cropVal*h):h,0:w]
    return img

def preprocess(img):
    img = cv2.resize(img,(0,0),None,0.5,0.5)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3, 3), 2, 0)

    img = cv2.Canny(img, 50, 150)
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.dilate(img, kernel)
    return img

def findContours(img):
    bboxs = []
    h,w = img.shape
    imgContours = np.zeros((h,w,3), np.uint8)
    contours, hierarchy =  cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(255,0,255),3) 
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        
        if area > 10000 and area < 250000:
            cv2.drawContours(imgContours, contours, i, (255, 0, 255), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(imgContours, (x, y), (x + w, y + h), (0, 255, 0), 1)
            bboxs.append((x, y, w, h))

    return imgContours,bboxs