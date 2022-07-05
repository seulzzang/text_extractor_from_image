# encoding: utf-8
from pytesseract import *
import cv2
import numpy as np
from imutils.perspective import four_point_transform
from imutils.contours import sort_contours
import imutils
import re
from datetime import datetime
#이미지 불러오기
image = cv2.imread(r"C:\Users\w0w12\Desktop\data2.jpg",cv2.IMREAD_COLOR)

# 이미지 전처리
## 첫 큰 사각형을 주민등록증 외곽으로 판단
def scan_img(image, width,ksize=(3,3), min_threshold=100, max_threshold=200):
    org_img = image.copy()
    image = imutils.resize(image, width=width)
    ratio = org_img.shape[1] / float(image.shape[1])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    chahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4,4))
    gray = chahe.apply(gray)

    blurred = cv2.GaussianBlur(gray, ksize, 0)
    blurred = cv2.Canny(blurred, min_threshold,max_threshold)
    cnts = cv2.findContours(blurred.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if len(approx) ==4:
            findCnt = approx
            transform_img = four_point_transform(org_img, findCnt.reshape(4, 2) * ratio)
            return transform_img
        else:
            return org_img


## text를 좀 더 정확하게 가져오기 위해 이미지 화질 개선
def img_roi(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel= cv2.getStructuringElement(cv2.MORPH_RECT, (12, 14))

    gray = cv2.GaussianBlur(gray, (9, 9), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    grad = cv2.Laplacian(blackhat, ddepth=cv2.CV_32F,ksize=3)
    grad = np.absolute(grad)
    (minVal, maxVal) = (np.min(grad), np.max(grad))
    grad = (grad - minVal) / (maxVal - minVal)
    grad = (grad * 255).astype("uint8")

    grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    close_thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    close_thresh = cv2.erode(close_thresh, None, iterations=2)

    cnts = cv2.findContours(close_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="top-to-bottom")[0]

    roi_list = []
    margin = 9
    image_grouping = image.copy()

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w // float(h)

        if ar == 7 : #이름
            color = (0, 255, 0)
            roi = image[y - margin:y + h + margin, x - margin:x + w + margin]
            roi_list.append(roi)

        elif ar== 5 : #생일
            color = (255,0,0)

        elif ar >=3 and ar <=4: #주소
            color = (255,255,0)
        else:
            color = (0, 0, 255)

        f =cv2.rectangle(image_grouping, (x - margin, y - margin), (x + w + margin, y + h + margin), color, 2)

    return f

image1 =scan_img(image ,width=200,ksize=(3,3), min_threshold=20,max_threshold=210)
gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
chahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(5, 5))
gray = chahe.apply(gray)
blurred = cv2.GaussianBlur(gray, (3,3), 0)



#def scaler_imag():
roi_img = img_roi(image1)
cv2.imshow("img_edge",roi_img)
cv2.waitKey(0)

# 전처리한 이미지로 텍스트 추출
text = image_to_string(blurred, lang='kor',config ='--psm 1 -c preserve_interword_spaces=1')
print(text)
