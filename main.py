# encoding: utf-8
from pytesseract import *
from PIL import Image
import cv2
import numpy as np
from imutils.perspective import four_point_transform
from imutils.contours import sort_contours
import imutils

#이미지 불러오기
#image = Image.open("C:\\Users\\w0w12\\Desktop\\hs_주민등록증_for_data1.jpg")
#image_nparray = np.asarray("C:/Users/w0w12/Desktop/hs_주민등록증_for_data1.jpg",dtype= np.uint8)
image = cv2.imread(r"C:\Users\w0w12\Desktop\data2.jpg",cv2.IMREAD_COLOR)
#print(image_nparray.shape)
# print(image.shape)
# 이미지 전처리
## 첫 큰 사각형을 주민등록증 외곽으로 판단
## 주민등록증 외곽을 기준으로 이미지 보정
def scan_img(image, width,ksize=(1,1), min_threshold=190, max_threshold=210):
    org_img = image.copy()
    image = imutils.resize(image, width=width)
    ratio = org_img.shape[1] / float(image.shape[1])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    chahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(1,1))
    gray = chahe.apply(gray)

    blurred = cv2.GaussianBlur(gray, ksize, 0)
    edged= cv2.Canny(blurred, min_threshold,max_threshold)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    findCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)

        if len(approx)==4:
            findCnt = approx
            break

    if findCnt is None :
        print("Could not find outline.")

    transform_img = four_point_transform(org_img, findCnt.reshape(4,2)* ratio)
    return transform_img



image_scan = scan_img(image,width=200,ksize=(1,1), min_threshold=180,max_threshold=210)
# 전처리한 이미지로 텍스트 추출
print01 = image_to_string(image_scan, lang='kor',config ='--psm 1 -c preserve_interword_spaces=1')
print(print01)
# # print(pt.image_to_string(image,lang='kor',config= '-c preserve_interword_spaces=1 --psm 4'))

#추출한 텍스트 word에 올리기 : wordmk.py