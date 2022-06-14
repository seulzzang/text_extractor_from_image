# encoding: utf-8
from pytesseract import *
from PIL import Image

image = Image.open("C:\\Users\\w0w12\\Desktop\\hs_주민등록증_for_data1.jpg")

print01 = image_to_string(image, lang='kor',config ='--psm 12 -c preserve_interword_spaces=1')
print(print01)
# print(pt.image_to_string(image,lang='kor',config= '-c preserve_interword_spaces=1 --psm 4'))

