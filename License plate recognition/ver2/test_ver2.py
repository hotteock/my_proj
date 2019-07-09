import cv2
import numpy as np
import pytesseract
from  PIL import Image
import matplotlib.pyplot as plt

import Preprocess
import PossibleChar
#import DetectChars

img = cv2.imread('1.jpg', cv2.IMREAD_COLOR)

listOfPossiblePlates = []

height, width, numChannels = img.shape

imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
imgThreshScene = np.zeros((height, width, 1), np.uint8)
imgContours = np.zeros((height, width, 3), np.uint8)

imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

imgTopHat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, structuringElement)
imgBlackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, structuringElement)

imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
gray = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)

img_thresh = cv2.adaptiveThreshold(
    img_blurred,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
)

#########################################################################Preprocesssing


imgThreshCopy = imgThreshScene.copy()
contours, npHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

temp_res = np.zeros((height, width, numChannels), dtype=np.uint8)

cv2.drawContours(temp_res, contours=contours, contourIdx = -1, color = (255,255,255))


temp_res = np.zeros((height, width, numChannels), dtype=np.uint8)

contours_dict = []

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(temp_res, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)

    # insert to dict
    contours_dict.append({
        'contour': contour,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'cx': x + (w / 2),
        'cy': y + (h / 2)
    })


MIN_AREA = 80
MIN_WIDTH, MIN_HEIGHT = 2, 2
MIN_RATIO, MAX_RATIO = 0.25, 1.0

possible_contours = []

cnt = 0
for d in contours_dict:
    area = d['w'] * d['h']
    ratio = d['w'] / d['h']

    if area > MIN_AREA and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT and MIN_RATIO < ratio < MAX_RATIO:
        d['idx'] = cnt
        cnt += 1
        possible_contours.append(d)

print(len(possible_contours))


temp_res3 = np.zeros((height, width, numChannels), dtype=np.uint8)

for d in possible_contours:
    cv2.rectangle(temp_res3, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255, 255, 255), thickness=2)


plt.imsave('rect3.jpg', temp_res3, cmap='gray')

#cv2.imwrite('rect.jpg', temp_res)


###############################################################Select candidate by 'char size'

MAX_DIAG_MULTIPLYER = 5
MAX_ANGLE_DIFF = 12.0
MAX_AREA_DIFF = 0.5
MAX_WIDTH_DIFF = 0.8
MAX_HEIGHT_DIFF = 0.2
MIN_N_MATCHED = 3


def find_chars(contour_list):
    matched_res_idx = []

    for d1 in contour_list:
        matched_contours_idx = []
        for d2 in contour_list:
            if d1['idx'] == d2['idx']:
                continue

            dx = abs(d1['cx'] - d2['cx'])
            dy = abs(d1['cy'] - d2['cy'])

            diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)

            distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
            if dx == 0:
                angle_diff = 90
            else:
                angle_diff = np.degrees(np.arctan(dx/dy))

            area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
            width_diff = abs(d1['w'] - d2['w']) / d1['w']
            height_diff = abs(d1['h'] - d2['h']) / d1['h']

            if distance < diagonal_length1 * MAX_DIAG_MULTIPLYER \
                and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
                and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                    matched_contours_idx.append(d2['idx'])

        matched_contours_idx.append(d1['idx'])

        if len(matched_contours_idx) < MIN_N_MATCHED:
            continue

        matched_res_idx.append(matched_contours_idx)

        unmatched_contour_idx = []

        for d4 in contour_list:
            if d4['idx'] not in matched_contours_idx:
                unmatched_contour_idx.append(d4['idx'])

        unmatched_contour = np.take(possible_contours, unmatched_contour_idx)

        recursive_contour_list = find_chars(unmatched_contour)

        for idx in recursive_contour_list:
            matched_contours_idx.append(idx)
        break

    return matched_res_idx


result_idx = find_chars(possible_contours)

matched_res = []
for idx_list in result_idx:
    matched_res.append(np.take(possible_contours, idx_list))


temp_res = np.zeros((height, width, numChannels), dtype=np.uint8)

for r in matched_res:
    for d in r:
        cv2.rectangle(temp_res, (d['x'], d['y']), (d['x']+d['w'], d['y']+d['h']), (255, 255, 255), 2)







