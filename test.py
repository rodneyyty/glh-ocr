from PIL import Image
import pytesseract
import filters

from PIL import Image
import pytesseract

textFilters = filter(lambda x: x.find("__") == -1, dir(filters))
im = Image.open("./test.jpg")

text = pytesseract.image_to_string(im, lang = 'eng')

for filterName in textFilters:
    f = getattr(filters, filterName)
    text = f(text)

print(text)
