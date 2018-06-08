import os, base64
from qgis.core import *
from qgis.utils import *

@qgsfunction(args='auto', group='Lanzen')
def show_scan(url, mimeType, feature, parent):
	QgsMessageLog.logMessage('show_scan: url: ' + url + ', mimeType: ' + mimeType, 'Lanzen', level=Qgis.Info)
	svg = """<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g><image xlink:href="data:image/{0};base64,{1}" height="64" width="80" /></g></svg>"""
	imagePath = url[8:] ##the URL must be the local one with 'file:' protocol
	QgsMessageLog.logMessage('show_scan: imagePath: ' + imagePath, 'Lanzen', level=Qgis.Info)
	path = imagePath + '.svg'
	QgsMessageLog.logMessage('show_scan: path: ' + path, 'Lanzen', level=Qgis.Info)
	if os.path.exists(path):
		return path
	with open(imagePath, "rb") as imageFile:
		data = base64.b64encode(imageFile.read())
		newsvg = svg.format(mimeType.lower(), data).replace("b'", "'", 1).replace('\n','')
	with open(path, 'w') as f:
		f.write(newsvg)
	return path
