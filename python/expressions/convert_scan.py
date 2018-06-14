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
	thumbnailSize = 128, 128
	targetExtension = '.png'
	targetUrl = url + targetExtension
	sourcePath = url[8:] ##the URL must be the local one with 'file:' protocol
	targetPath = sourcePath + targetExtension
	if os.path.exists(targetPath):
		return targetUrl
	elif not os.path.exists(sourcePath):
		return None
	image = Image.open(sourcePath) 
	image.thumbnail(thumbnailSize)
	image.save(targetPath)
	#QgsMessageLog.logMessage('converted to: ' + targetUrl, 'Lanzen', level=Qgis.Info)
	return targetUrl
