import cv2
import numpy as np
import pytesseract
from  PIL import Image

class num_rcg:
    def Ext_num(self):
        img = cv2.imread('num1.jpg', cv2.IMREAD_COLOR)
        copy_img = img.copy()
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur = cv2.bilateralFilter(img2, 5, 70, 70)
        #blur = cv2.GaussianBlur(img2, (3,3),0)
        cv2.imwrite('blur.jpg', blur)

        canny = cv2.Canny(blur, 100, 200)
        cv2.imwrite('canny.jpg', canny)

        contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        boxes = []

        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            x,y,w,h = cv2.boundingRect(cnt)
            rect_area = w*h
            aspect_ratio = float(w)/h

            if(aspect_ratio >= 0.1) and (aspect_ratio <= 3.0) and (rect_area >= 70) and(rect_area <= 850):
                cv2.rectangle(img,(x,y), (x+w, y+h), (0, 255, 0), 1)
                boxes.append(cv2.boundingRect(cnt))

        cv2.imwrite('tst.jpg', img)
        a=1
        return(a)

recogtest = num_rcg()
result=recogtest.Ext_num()
