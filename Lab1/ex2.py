import numpy as np
from PIL import Image

image = Image.open("imagem.jpg")
image_data = np.asarray(image)

with open('svgfile.svg', 'a') as svgfile:
    svgfile.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n')

    for i in range(len(image_data)):
        for j in range(len(image_data[0])):
            radius = (255 - image_data[i][j])/255
            svgfile.write("<circle r=\"" + str(radius) + "\" cx=\"" + str(j) + "\" cy=\"" + str(i) + "\" />")
        
        
    svgfile.write('</svg>')
