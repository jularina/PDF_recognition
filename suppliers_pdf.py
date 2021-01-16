# coding: utf-8

from pdf2image import convert_from_path 
from matplotlib import pyplot as plt
from PIL import Image
import pytesseract
import argparse
import cv2
import os


pytesseract.pytesseract.tesseract_cmd = ( r"C:\Program Files (x86)\Tesseract-OCR\tesseract")
images = convert_from_path('PO17-10.pdf')

for img in images: 
    img.save('output.jpg', 'JPEG')

image = cv2.imread('output.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

filename = "out.png"
cv2.imwrite(filename, gray)
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)

plt.figure(figsize=(15,15))
plt.imshow(image)
plt.show()

print(text)