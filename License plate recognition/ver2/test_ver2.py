import cv2
import numpy as np
import pytesseract
from  PIL import Image

import Preprocess

class num_rcg:
    def Ext_num(self):
        img = cv2.imread('num4.jpg', cv2.IMREAD_COLOR)

        listOfPossiblePlates = []

        height, width, numChannels = img.shape

        imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
        imgThreshScene = np.zeros((height, width, 1), np.uint8)
        imgCountours = np.zeros((height, width, 3), np.uint8)

        imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(img)

        listOfPossibleChars = []
        intCountofPossibleChars = 0
        imgThreshCopy = imgThreshScene.copy()
        contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        imgCountours = np.zeros((height, width, 3), np.uint8)

        #for i in range(0, len(contours)):



        cv2.imwrite('t2_gray.jpg', imgGrayscaleScene)
        cv2.imwrite('t2_threshold.jpg', imgThreshScene)

        a=1
        return(a)


recogtest = num_rcg()
result=recogtest.Ext_num()