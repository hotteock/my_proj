import cv2
import numpy as np
import pytesseract
from  PIL import Image

class num_rcg:
    def Ext_num(self):
        img = cv2.imread('num3.jpg', cv2.IMREAD_COLOR)
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

        #sorted(boxes)

        for i in range(len(boxes)):  ##Buble Sort on python
            for j in range(len(boxes) - (i + 1)):
                if boxes[j][0] > boxes[j + 1][0]:
                    temp = boxes[j]
                    boxes[j] = boxes[j + 1]
                    boxes[j + 1] = temp

        f_count = 0
        select = 0
        plate_width = 0

        for i in range(len(boxes)):
            count = 0
            for j in range(i+1, (len(boxes)-1)):
                dx = abs(boxes[j+1][0]-boxes[i][0])
                if dx>150:
                    break
                dy=abs(boxes[j+1][1]-boxes[i][1])
                if dx ==0:
                    dx=1
                if dy==0:
                    dy=1
                grad = float(dy)/float(dx)
                if grad<0.25:
                    count = count+1
            if count>f_count:
                select = i
                f_count = count
                plate_width = dx

        number_plate = copy_img[boxes[select][1] - 10:boxes[select][3] + boxes[select][1] + 20,
                       boxes[select][0] - 10:140 + boxes[select][0]]

        cv2.imwrite('tt.jpg', number_plate)

        cv2.imwrite('tst.jpg', img)
        a=1
        return(a)

recogtest = num_rcg()
result=recogtest.Ext_num()