# encoding: utf-8
from pytesseract import *
from PIL import Image
import cv2
import numpy as np
from imutils.perspective import four_point_transform
from imutils.contours import sort_contours
import imutils

#이미지 불러오기
image = Image.open("C:\\Users\\w0w12\\Desktop\\hs_주민등록증_for_data1.jpg")

# 이미지 전처리
## 첫 큰 사각형을 주민등록증 외곽으로 판단
## 주민등록증 외곽을 기준으로 이미지 보정



# 전처리한 이미지로 텍스트 추출
print01 = image_to_string(image, lang='kor',config ='--psm 4 -c preserve_interword_spaces=1')
print(print01)
# print(pt.image_to_string(image,lang='kor',config= '-c preserve_interword_spaces=1 --psm 4'))

#추출한 텍스트 word에 올리기 : wordmk.py