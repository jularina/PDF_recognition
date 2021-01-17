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
image = "PO18-3.pdf"
images = convert_from_path(image)
for i, img in enumerate(images):
    jpgs_list.append(image[:-4] + '_output' + str(i) + '.jpg')
    img.save(image[:-4] + '_output' + str(i) + '.jpg', 'JPEG')

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

# show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)

# processing texts
text_items = text[(text.find('TOTAL PRICE') + 11):]
text_items = text_items[:(text_items.find('Total USD'))]

lines = text_items.splitlines()
non_empty_lines = [line for line in lines if line.strip() != ""]

items_list = set()
text_items = ''
for line in non_empty_lines:
    if line[0].isdigit() and line[1] == ' ':
        items_list.add(text_items)
        text_items = line[2:]
    else:
        text_items += line

items_list.add(text_items)
print(items_list)

# processing 1st condition
items_new = list(items_list).copy()
for i, item in enumerate(items_list):
    if 'USD' not in item and i == 0:
        items_new[i+1] = item + items_new[i+1]
        items_new.remove(item)
    elif 'USD' not in item and i != 0:
        items_new[i - 1] = item + items_new[i - 1]
        items_new.remove(item)

print(items_new)