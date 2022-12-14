import cv2 as cv
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

#we process chosen part of the screen the way that it would be easier for pytessect to get text from it
def get_text(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    invert = 255 - thresh
    try:
        text = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
    except:
        text = 'error'
    return text