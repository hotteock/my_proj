import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img = cv2.imread('1.jpg')

height, width, numChannels = img.shape

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

"""ret, thr1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
ret, thr2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
ret, thr3 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
ret, thr4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
ret, thr5 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)

cv2.imshow('origin', img)
cv2.imshow('binary', thr1)
cv2.imshow('binary_inv', thr2)
cv2.imshow('trunc', thr3)
cv2.imshow('tozero', thr4)
cv2.imshow('tozero_inv', thr5)

####################################### simple thresholding #############################


img_result2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 5)
img_result3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)

cv2.imshow('1', img_result2)
cv2.imshow('2', img_result3)


################################### adaptive thresholding ###########################

img_blur = cv2.GaussianBlur(img, (7,7), 0)
ret, img_result3 = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

cv2.imshow('3', img_result3)

################################### OTSU ############################################
"""

def hough(thr, img):
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi/180, thr)


kernel = np.ones((1, 1), np.uint8)
result = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

result2 = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5)

kernel2 = np.ones((1, 1), np.uint8)
result3 = cv2.morphologyEx(result2, cv2.MORPH_CLOSE, kernel)

contours, npHierarchy = cv2.findContours(result3, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

temp_res = np.zeros((height, width, numChannels), dtype=np.uint8)

cv2.drawContours(temp_res, contours=contours, contourIdx = -1, color = (255,255,255))

cv2.imshow('1', result)
cv2.imshow('2', result2)
cv2.imshow('3', result3)
cv2.imshow('contour', temp_res)

cv2.waitKey(0)
cv2.destroyAllWindows()

