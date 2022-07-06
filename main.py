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

# 고정된 영역 가져오기
def img_roi(image):
    # org_img = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel= cv2.getStructuringElement(cv2.MORPH_RECT, (16, 11))

    gray = cv2.GaussianBlur(gray, (9, 9), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    grad = cv2.Laplacian(blackhat, ddepth=cv2.CV_32F,ksize=3)
    grad = np.absolute(grad)
    (minVal, maxVal) = (np.min(grad), np.max(grad))
    grad = (grad - minVal) / (maxVal - minVal)
    grad = (grad * 255).astype("uint8")

    #grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    close_thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    close_thresh = cv2.erode(close_thresh, None, iterations=2)

    cnts = cv2.findContours(close_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="top-to-bottom")[0]

    name_list = []
    birthday_list = []
    address_list = []

    margin = 8
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w // float(h)
        if ar == 7:
            name_roi = image[y-margin: y+h+margin, x-margin: x+w+margin]
            name_list.append(name_roi)

        elif ar == 5 :
            birthday_roi = image[y-margin: y+h+margin, x-margin: x+w+margin]
            birthday_list.append(birthday_roi)

        elif ar >=3 and ar <=4:
            address_roi = image[y-margin: y+h+margin, x-margin: x+w+margin]
            address_list.append(address_roi)

    total_list = [name_list, birthday_list, address_list]
    return total_list

def img_to_str(roi):
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.normalize(gray_roi, None, 0, 255, cv2.NORM_MINMAX)
    chahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(5, 5))
    gray = chahe.apply(gray_roi)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    text = image_to_string(blurred, lang='kor', config='--psm 1')
    return text


## text를 좀 더 정확하게 가져오기 위해 이미지 화질 개선
image1 =scan_img(image ,width=200,ksize=(3,3), min_threshold=100,max_threshold=210)
gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
chahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(5, 5))
gray = chahe.apply(gray)
blurred = cv2.GaussianBlur(gray, (3,3), 0)
text = image_to_string(blurred, lang='kor',config ='--psm 1 -c preserve_interword_spaces=1')
print(text)


# 전처리한 이미지로 텍스트 추출
image1 =scan_img(image,width=200,ksize=(3,3), min_threshold=150,max_threshold=210)
name_list = img_roi(image1)[0]
birthday_list = img_roi(image1)[1]
address_list = img_roi(image1)[2]
print(name_list)
print(birthday_list)
print(address_list)

name = img_to_str(name_list)
print(name)


# name = image_to_string(name_roi , lang='kor',config ='--psm 1 -c preserve_interword_spaces=1')
# obirthday = image_to_string(birthday_roi, lang='kor',config ='--psm 1 -c preserve_interword_spaces=1')
address = image_to_string(address_list, lang='kor',config ='--psm 1')
print(address)
# date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# name_list = re.findall(r"\w{3}",text)
# birthdate_list = re.findall(r"\d{6}", text)
# address_list = re.findall(r"\w+시\b \w+구\b",text)
# date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(name_list)
# print(birthdate_list)
# print(address_list)
# print(date)

#텍스트 word에 올리기
#from docx import Document

# doc = Document()
#
# table = doc.add_table(rows = 1, cols=4)
# table.style = doc.styles['Table Grid']
#
# first_row = table.rows[0].cells
#
# first_row[0].text = '이름'
# first_row[1].text = '생년월일'
# first_row[2].text = '주소'
# first_row[3].text = '업로드 된 시간'
#
# row_cells = table.add_row().cells
# row_cells[0].text = name
# row_cells[1].text = birthday
# row_cells[2].text = address
# row_cells[3].text = date
# doc.save('ImageInformation.docx')
