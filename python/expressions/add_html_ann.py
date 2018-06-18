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

import os
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.PyQt.QtCore import QSizeF
from qgis.PyQt.QtGui import (QFont, QTextDocument)
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
	if layer.selectedFeatureCount():
		features = layer.selectedFeatures()
	else:
		features = layer.getFeatures()
	for f in features:
		context.setFeature(f)
		createScanExpression = QgsExpression('convert_scan("Erste_Fund_Abbildung_URL")')
		imageUrl = createScanExpression.evaluate(context)
		_add(imageUrl, layer, f)
	# If caching is enabled, a simple canvas refresh might not be sufficient
	# to trigger a redraw and you must clear the cached image for the layer
	if iface.mapCanvas().isCachingEnabled():
		layer.triggerRepaint()
	else:
		iface.mapCanvas().refresh()

def _add(imageUrl, layer, feature):
	QgsMessageLog.logMessage('_add: ' + imageUrl, 'Lanzen', level=Qgis.Info)
	if not imageUrl: #nothing to do if there is no image to display
		return
	imagePath = imageUrl[8:]
	if not os.path.exists(imagePath):
		return
	for a in QgsProject.instance().annotationManager().annotations():
		QgsMessageLog.logMessage('ann: layer: {0}, feature: {1}'.format(a.mapLayer(), a.associatedFeature()) , 'Lanzen', level=Qgis.Info)
	annotation = QgsTextAnnotation()
	annotation.setMapLayer(layer)
	annotation.setAssociatedFeature(feature)
	#generate the HTML content
	doc = QTextDocument()
	font = QFont()
	font.setFamily('Times New Roman')
	doc.setDefaultFont(font)
	doc.setHtml('<img src="{}" />'.format(imageUrl))
	annotation.setDocument(doc)
	annotation.markerSymbol().setSize(0)
	annotation.setHasFixedMapPosition(True)
	annotation.setMapPosition(feature.geometry().asPoint())
	# we only need dimensions here to resize the annotation
	with Image.open(imagePath) as image:
		width, height=image.size
		annotation.setFrameSize(QSizeF(width, (height + 5)))
	QgsProject.instance().annotationManager().addAnnotation(annotation)
