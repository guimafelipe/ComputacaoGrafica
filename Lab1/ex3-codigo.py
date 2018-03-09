import numpy as np
import colorsys


with open('color-selector.svg', 'a') as svgfile:
    svgfile.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n')

    for i in range(25):
        for j in range(25):
            (r, g, b) = colorsys.yiq_to_rgb(0.5, (10*i - 127)/128, (10*j - 127) / 128)
            svgfile.write("<circle r=\"5\" cx=\"" + str(5 + 10*j) + "\" cy=\"" + str(5+ 10*i) + "\" fill=\"rgb(" + str(255*r) + "," + str(255*g) + "," + str(255*b) + ")\" onclick=\"document.getElementById('mainbox').setAttribute('fill','rgb(" + str(255*r) + "," + str(255*g) + "," + str(255*b) + "');\"/>\n")
    
    svgfile.write("<rect id=\"mainbox\" x=\"0\" y=\"250\" width=\"250\" height=\"10\" />")
        
    svgfile.write('</svg>')
