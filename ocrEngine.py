import pytesseract

#Vars
config      = '--psm 10 -c tessedit_char_whitelist=123456789'

def getChar(img):
    return pytesseract.image_to_string(img, config=config, timeout=1)