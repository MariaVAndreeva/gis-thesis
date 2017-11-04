import os, base64
from qgis.core import *

@qgsfunction(args='auto', group='Custom')
def show_scan(url, mimeType, feature, parent):
    svg = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg><g>
    <image xlink:href="data:image/{0};base64,{1}" height="256" width="320" />
</g></svg>
"""
    imagePath = url[8:] ##the URL must be the local one with 'file:' protocol
    path = imagePath + '.svg'
    if os.path.exists(path):
        return path
    with open(imagePath, "rb") as imageFile:
        data = base64.b64encode(imageFile.read())
        newsvg = svg.format(mimeType.lower(), data).replace('\n','')
    with open(path, 'w') as f:
        f.write(newsvg)
    return path
