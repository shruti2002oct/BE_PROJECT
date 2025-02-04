
import cv2
import numpy as np
from FindBalloon import *
from detectHit import *
from calbi import *
# Read the original image
img = cv2.imread('test3.png') 
# Display original image
points = pickle.load(open('calibration.pkl','rb'))
img = getBoard(img,points)
imgBallons, bboxs = findBalloons(img)
img = detectHit(img ,bboxs)
# Convert to graycsale  


# Display Sobel Edge Detection Images
cv2.imshow('Sobel X', imgBallons)
cv2.waitKey(0)

 
cv2.destroyAllWindows()