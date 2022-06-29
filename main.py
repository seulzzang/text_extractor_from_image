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
#image = Image.open("C:\\Users\\w0w12\\Desktop\\hs_주민등록증_for_data1.jpg")
#image_nparray = np.asarray("C:/Users/w0w12/Desktop/hs_주민등록증_for_data1.jpg",dtype= np.uint8)
image = cv2.imread(r"C:\Users\w0w12\Desktop\data2.jpg",cv2.IMREAD_COLOR)
#print(image_nparray.shape)
# print(image.shape)
# 이미지 전처리
## 첫 큰 사각형을 주민등록증 외곽으로 판단
## 주민등록증 외곽을 기준으로 이미지 보정
def scan_img(image, width,ksize=(3,3), min_threshold=100, max_threshold=200):
    org_img = image.copy()
    image = imutils.resize(image, width=width)
    ratio = org_img.shape[1] / float(image.shape[1])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    chahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
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



image_scan = scan_img(image,width=200,ksize=(3,3), min_threshold=180,max_threshold=210)
# 전처리한 이미지로 텍스트 추출
text = image_to_string(image_scan, lang='kor',config ='--psm 1 -c preserve_interword_spaces=1')
text = re.sub("\s\d\s","",text)

print(text)

# # print(pt.image_to_string(image,lang='kor',config= '-c preserve_interword_spaces=1 --psm 4'))
# print(text[2])
#추출한 텍스트 word에 올리기
name = re.findall(r"\w{3}",text)[1]
#birthdate = re.findall(r"\d{6}", text)
birthdate = re.findall(r'[\+\(]?[1-9][0-9 ]{8,}[0-9]', text)
address = re.findall(r"\w+시\b \w+구\b",text)[0]
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(name)
print(birthdate)
print(address)
print(date)

from docx import Document

doc = Document()

table = doc.add_table(rows = 1, cols=4)
table.style = doc.styles['Table Grid']

first_row = table.rows[0].cells

first_row[0].text = '이름'
first_row[1].text = '생년월일'
first_row[2].text = '주소'
first_row[3].text = '업로드 된 시간'

row_cells = table.add_row().cells
row_cells[0].text = name
row_cells[1].text = '0'
row_cells[2].text = address
row_cells[3].text = date
doc.save('ImageInformation.docx')
