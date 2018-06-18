import os, sys
from qgis.core import *
from qgis.gui import *
from PIL import Image

@qgsfunction(args='auto', group='Lanzen')
def convert_scan(url, feature, parent):
	"""
	Converts an image at specified URL to PNG.
	<h2>Example usage:</h2>
	<ul>
		<li>convert_scan('file:///c:/tmp/a.tiff') -> 'file:///c:/tmp/a.tiff.png'</li>
		<li>convert_scan("fieldURL") -> -> 'file:///c:/tmp/a.tiff.png'</li>
	</ul>
	"""
	QgsMessageLog.logMessage('convert_scan: ' + url, 'Lanzen', level=Qgis.Info)
	defaultSize = 64, 64
	targetExtension = '.png'
	targetUrl = url + targetExtension
	sourcePath = url[8:] # the URL must be the local one with 'file:' protocol
	targetPath = sourcePath + targetExtension
	if os.path.exists(targetPath):
		return targetUrl
	elif not os.path.exists(sourcePath):
		return None
	scale = evalScale(feature)
	thumbnailSize = tuple([scale * x for x in defaultSize])
	image = Image.open(sourcePath)
	image.thumbnail(thumbnailSize)
	image.save(targetPath)
	QgsMessageLog.logMessage('convert_scan: resulting image: ' + targetUrl, 'Lanzen', level=Qgis.Info)
	return targetUrl

def evalScale(feature):
	# Some safety checks
	scaleExpression = feature['Erste_Fund_Abbildung_Skalierung']
	#QgsMessageLog.logMessage('scaleExpression: ' + scaleExpression, 'Lanzen', level=Qgis.Info)
	assert len(scaleExpression) < 1024
	try:
		return 1 / eval(scaleExpression.replace(':', '/'))
	except Exception as e:
		QgsMessageLog.logMessage('scale evaluation failed: {}'.format(e), 'Lanzen', level=Qgis.Error)
	return 1
