from PIL import Image
import pytesseract

from PIL import Image
import pytesseract

im = Image.open("./test.jpg")

text = pytesseract.image_to_string(im, lang = 'eng')

print(text)
