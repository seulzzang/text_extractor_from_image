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
## 주민등록증 외곽을 기준으로 이미지 보정
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

