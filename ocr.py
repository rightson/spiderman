import re
from PIL import Image
import pytesseract


def png2String(file):
    img = Image.open(file)
    img = img.convert('L')
    return pytesseract.image_to_string(img)


def png2Integer(file):
    string = png2String(file)
    return re.sub('[^\\d]', '', string)
