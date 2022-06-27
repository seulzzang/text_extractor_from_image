# encoding: utf-8
#추출한 텍스트 word에 올리기
from docx import Document

doc = Document()

table = doc.add_table(rows = 1, cols=4)
table.style = doc.styles['Table Grid']

first_row = table.rows[0].cells

first_row[0].text = '이름'
first_row[1].text = '생년월일'
first_row[2].text = '주소'
first_row[3].text = '업로드 된 시간'

doc.save('ImageInformation.docx')