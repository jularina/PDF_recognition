# coding: utf-8

from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import cv2
import os

# set directory
pytesseract.pytesseract.tesseract_cmd = (r"C:\Program Files (x86)\Tesseract-OCR\tesseract")
folder = r'C:\Users\Arina27\Desktop\Arina\diplom\data\pdfminer' + '\\'
os.chdir(folder)

# save pdf as jpg (if there are several pages --> img for each)
jpgs_list, texts_list = [], []
image = "PO17-10.pdf"
images = convert_from_path(image)
for i, img in enumerate(images):
    jpgs_list.append(image[:-4]+'_output'+str(i)+'.jpg')
    img.save(image[:-4]+'_output'+str(i)+'.jpg', 'JPEG')

# load image and convert to grayscale
image = cv2.imread(jpgs_list[0])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # perform a threshold in order to segment the foreground from the background
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# # write the grayscale image to disk as a temporary file so we can apply OCR to it
filename = jpgs_list[0][:-4] + ".png"
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
texts_list.append(text)

# processing texts
text_items = text[(text.find('TOTAL PRICE')+11):]
text_items = text_items[:(text_items.find('Total USD'))]
print(text_items.splitlines())

# show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)