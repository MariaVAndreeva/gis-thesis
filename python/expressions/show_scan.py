import sys, os, base64
from qgis.core import *
from qgis.utils import *

@qgsfunction(args='auto', group='Lanzen')
def show_scan(url, mimeType, feature, parent):
	svg = """<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g><image xlink:href="data:image/{0};base64,{1}" height="64" width="80" /></g></svg>"""
	imagePath = url[8:] # the URL must be the local one with 'file:' protocol
	path = imagePath + '.svg'
	if os.path.exists(path):
		QgsMessageLog.logMessage('image exists at: ' + path, 'Lanzen', level=Qgis.Info)
		return path
	QgsMessageLog.logMessage('creating a new image at: ' + path, 'Lanzen', level=Qgis.Info)
	with open(imagePath, "rb") as imageFile:
		data = base64.b64encode(imageFile.read())
		newsvg = svg.format(mimeType.lower(), data).replace("b'", "'", 1).replace('\n','')
	with open(path, 'w') as f:
		f.write(newsvg)
	return path
