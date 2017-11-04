import os, base64
from qgis.core import *

@qgsfunction(args='auto', group='Custom')
def show_scan(url, feature, parent):
    svg = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg><g>
    <image xlink:href="data:image/tiff;base64,{0}" height="256" width="320" />
</g></svg>
"""
    imagePath = url[8:]
    path = imagePath + '.svg'
    if os.path.exists(path):
        return path
    with open(imagePath, "rb") as imageFile:
        data = base64.b64encode(imageFile.read())
        newsvg = svg.format(data).replace('\n','')
    with open(path, 'w') as f:
        f.write(newsvg)
    return path
