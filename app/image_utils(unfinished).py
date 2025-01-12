from PIL import Image
try:
    im = Image.open("app/static/img/gramineae poaceae (grass)/grass-Poa pratense001.jpg")
    im.show()
except FileNotFoundError:
    print("File not found")

"""Drawing bounding box for images based on annotations coordinates"""