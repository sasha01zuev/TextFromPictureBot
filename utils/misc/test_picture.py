import cv2
import pytesseract
import numpy as np

"""Testing pictures"""
picture = '/home/alex/Рабочий стол/Telegram/TFPBot/pictures/picture.png'


# get grayscale image
def get_grayscale(image):
    return cv2.imread(image, 0)


# thresholding
def thresholding(image):
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((1, 2), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


gray = get_grayscale(picture)
thresh = thresholding(gray)
dilate = dilate(thresh)
erode = erode(thresh)
# opening = opening(erode)
# canny = canny(opening)

output_text = pytesseract.image_to_string(thresh, lang='eng+rus+ukr', config='--oem 3 --psm 6')
print(output_text)
cv2.imshow('picture', thresh)
cv2.waitKey()
