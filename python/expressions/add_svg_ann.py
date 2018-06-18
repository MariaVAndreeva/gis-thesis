from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from PyQt5.QtCore import QSizeF

@qgsfunction(args='auto', group='Lanzen')
def add_svg_ann(layerId, path, feature, parent):
	QgsMessageLog.logMessage('layerId: ' + layerId + ', path: ' + path, 'Lanzen', level=Qgis.Info)
	currentLayer = QgsProject.instance().mapLayer(layerId)
	svgAnnotation = QgsSvgAnnotation(iface.mapCanvas())
	svgAnnotation.setMapLayer(currentLayer)
	symbol = QgsMarkerSymbol()
	symbol.setSize(0)
	svgAnnotation.setMarkerSymbol(symbol)
	svgAnnotation.setHasFixedMapPosition(True)
	svgAnnotation.setMapPosition(feature.geometry().asPoint())
	svgAnnotation.setFrameSize(QSizeF(80, 64))
	svgAnnotation.setFilePath(path)
	QgsProject.instance().annotationManager().addAnnotation(svgAnnotation)
	# If caching is enabled, a simple canvas refresh might not be sufficient
	# to trigger a redraw and you must clear the cached image for the layer
	if iface.mapCanvas().isCachingEnabled():
		currentLayer.triggerRepaint()
	else:
		iface.mapCanvas().refresh()
	return
