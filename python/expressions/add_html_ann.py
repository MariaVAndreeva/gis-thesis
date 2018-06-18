# -*- coding: utf-8 -*-
"""
Define a new function using the @qgsfunction decorator.

The function accept the following parameters

:param [any]: Define any parameters you want to pass to your function before
			  the following arguments.
:param feature: The current feature
:param parent: The QgsExpression object
:param context: If there is an argument called ``context`` found at the last
				position, this variable will contain a ``QgsExpressionContext``
				object, that gives access to various additional information like
				expression variables. E.g. ``context.variable('layer_id')``
:returns: The result of the expression.


The @qgsfunction decorator accepts the following arguments:

:param args: Defines the number of arguments. With ``args='auto'`` the number
			 arguments will automatically be extracted from the signature.
:param group: The name of the group under which this expression function will
			  be listed.
:param usesgeometry: Set this to False if your function does not access
					 feature.geometry(). Defaults to True.
:param referenced_columns: An array of attribute names that are required to run
						   this function. Defaults to
						   [QgsFeatureRequest.ALL_ATTRIBUTES].
"""

import os, random, math
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.PyQt.QtCore import (QPointF,
											QSizeF)
from qgis.PyQt.QtGui import (QFont,
											QTextDocument)
from PIL import Image

@qgsfunction(args='auto', group='Lanzen')
def add_html_ann(feature, parent, context):
	"""
	Calculates the sum of the two parameters value1 and value2.
	<h2>Example usage:</h2>
	<ul>
		<li>my_sum(5, 8) -> 13</li>
		<li>my_sum("fiel1", "field2") -> 42</li>
	</ul>
	"""
	layer = QgsProject.instance().mapLayer(context.variable('layer_id'))
	points = [feat for feat in layer.getFeatures()]
	spatialIndex = QgsSpatialIndex() # this spatial index contains all the features of the point layer
	for point in points:
		spatialIndex.insertFeature(point)
	
	if layer.selectedFeatureCount():
		features = layer.selectedFeatures()
	else:
		features = layer.getFeatures()
	for f in features:
		geometry = f.geometry() #Input geometry
		idsList = spatialIndex.intersects(geometry.boundingBox())
		duplicatesIndex = idsList.index(f.id())
		duplicates = len(idsList) - 1
		context.setFeature(f)
		createScanExpression = QgsExpression('convert_scan("Erste_Fund_Abbildung_URL")')
		imageUrl = createScanExpression.evaluate(context)
		_add(imageUrl, layer, f, duplicates, duplicatesIndex)
	# If caching is enabled, a simple canvas refresh might not be sufficient
	# to trigger a redraw and you must clear the cached image for the layer
	if iface.mapCanvas().isCachingEnabled():
		layer.triggerRepaint()
	else:
		iface.mapCanvas().refresh()

def _add(imageUrl, layer, feature, duplicates, duplicatesIndex):
	#QgsMessageLog.logMessage('_add: {0}, {1}, duplicatesIndex: {2}'.format(imageUrl, duplicates, duplicatesIndex), 'Lanzen', level=Qgis.Info)
	if not imageUrl: #nothing to do if there is no image to display
		return
	imagePath = imageUrl[8:]
	if not os.path.exists(imagePath):
		return
	annotation = QgsTextAnnotation(iface.mapCanvas())
	annotation.setMapLayer(layer)
	annotation.setAssociatedFeature(feature)
	#generate the HTML content
	doc = QTextDocument()
	font = QFont()
	font.setFamily('Times New Roman')
	doc.setDefaultFont(font)
	doc.setHtml('{0}<img src="{2}" />'.format(feature.id(), duplicatesIndex, imageUrl))
	annotation.setDocument(doc)
	annotation.markerSymbol().setSize(0)
	annotation.setHasFixedMapPosition(True)
	annotation.setMapPosition(feature.geometry().asPoint())
	# we only need dimensions here to resize the annotation
	with Image.open(imagePath) as image:
		width, height=image.size
		annotation.setFrameSize(QSizeF((width * 1.1 + 3), (height + 18))) #leave room for text
		#now avoid overlapping for a single point
		if duplicates:
			radius = 12 * (duplicates + 1)
			theta = 2 * math.pi * duplicatesIndex / (duplicates + 1)
			x = radius * math.cos(theta)
			y = radius * math.sin(theta)
			if x < 0:
				x -= width
			if y < 0:
				y -= height
			annotation.setFrameOffsetFromReferencePoint(QPointF(x, y))
	QgsProject.instance().annotationManager().addAnnotation(annotation)
