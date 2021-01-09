import pytesseract

# Vars
config = '--psm 10 -c tessedit_char_whitelist=123456789'
pytesseract.pytesseract.tesseract_cmd = 'D:\\Private\\Juventus\\DataScience\\tesseract\\tesseract.exe'

def getChar(img):
    return pytesseract.image_to_string(img, config=config, timeout=1)
