# -*- coding: utf-8 -*-
"""
Generates pictures for printing using predefined downsize factor
"""

import os
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from PIL import Image

def evalScale(scaleExpression):
	if not scaleExpression:
		return 1
	assert len(scaleExpression) < 1024
	try:
		return 1 / eval(scaleExpression.replace(':', '/'))
	except Exception as e:
		QgsMessageLog.logMessage('scale evaluation failed: {}'.format(e), 'Lanzen', level=Qgis.Info)
	return 1

downsizeFactor = 9
project = QgsProject.instance()
layer = project.mapLayer('[% @layer_id %]')
if layer.selectedFeatureCount():
	features = layer.selectedFeatures()
else:
	features = layer.getFeatures()
for feature in features:
	url = feature["Erste_Fund_Abbildung_URL"]
	if not url:
		continue
	sourcePath = url[8:]
	if not os.path.exists(sourcePath):
		continue
	targetExtension = '.1-{}.png'.format(downsizeFactor)
	targetPath = sourcePath + targetExtension
	if os.path.exists(targetPath):
		continue
	scaleExpression = feature["Erste_Fund_Abbildung_Skalierung"]
	scale = evalScale(scaleExpression)
	with Image.open(sourcePath) as image:
		scanSize = width, height = image.size
		thumbnailSize = tuple([scale * x / downsizeFactor for x in scanSize])
		image.thumbnail(thumbnailSize)
		image.save(targetPath)
	