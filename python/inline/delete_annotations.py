# -*- coding: utf-8 -*-
"""
Deletes all annotations from the ciurrent layer.
One needs to save the project to persist the changes.

"""

from qgis.core import *
from qgis.gui import *
from qgis.utils import *

project = QgsProject.instance()
layer = project.mapLayer('[% @layer_id %]')
annotationManager = project.annotationManager()
layerAnnotations = list(filter(lambda a: a.mapLayer().id() == layer.id(), annotationManager.annotations()))
for ann in layerAnnotations:
	removed = annotationManager.removeAnnotation(ann)
