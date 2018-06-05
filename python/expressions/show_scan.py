import os, base64
from qgis.core import *
from qgis.utils import iface
from PyQt5.QtCore import QSizeF

@qgsfunction(args='auto', group='Custom')
def show_scan(url, mimeType, feature, parent):
	svg = """<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g><image xlink:href="data:image/{0};base64,{1}" height="256" width="320" /></g></svg>"""
	imagePath = url[8:] ##the URL must be the local one with 'file:' protocol
	path = imagePath + '.svg'
	if os.path.exists(path):
		return path
	with open(imagePath, "rb") as imageFile:
		data = base64.b64encode(imageFile.read())
		newsvg = svg.format(mimeType.lower(), data).replace("b'", "'", 1).replace('\n','')
	with open(path, 'w') as f:
		f.write(newsvg)
	#svgAnnotation = QgsSvgAnnotation(iface.mapCanvas())
	#symbol = QgsMarkerSymbol()
	#symbol.setSize(10)
	#svgAnnotation.setMarkerSymbol(symbol)
	#geom = feature.geometry()
	#point = geom.asPoint()
	#svgAnnotation.setMapPosition(point)
	#svgAnnotation.setMapLayer(iface.activeLayer())
	#svgAnnotation.setFrameSize(QSizeF(300, 200))
	#svgAnnotation.setFilePath(path)
	#canvas.refresh()
	return path
