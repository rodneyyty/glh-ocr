from PIL import Image
import pytesseract
import filters

from PIL import Image
import pytesseract

textFilters = filter(lambda x: x.find("__") == -1, dir(filters))
im = Image.open("./test.jpg")

text = pytesseract.image_to_string(im, lang = 'eng')
data = []

for filterName in textFilters:
    f = getattr(filters, filterName)
    response = f(text)
    if type(response) is str:
        text = response
    elif type(response) is list:
        data.append([filterName, response])
        text = response[0]

print('Result:')
print(text)
print('Data:')
print(map(lambda x: x[1:], data))
