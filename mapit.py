#!/usr/bin/python3

import yaml
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from qgis.core import QgsApplication, QgsProject, QgsCoordinateReferenceSystem, QgsVectorLayer, QgsRasterLayer, QgsMapSettings, QgsMapRendererParallelJob

with open("./MapMyCsv.yaml", "r") as f:
    config = yaml.safe_load(f)
    elipsoid = config['settings']['elipsoid']
    csvPath = config['settings']['csvPath']
    
    QgsApplication.setPrefixPath(config['settings']['prefixPath'], True)
    qgs = QgsApplication([], False)
    
    qgs.initQgis()
    wgs84="EPSG:4326"

    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem(elipsoid))

    # if you get a file imported as you want in the desktop application, you can hover over the layer
    # to gett the settings that are in the URI
    uri = 'file://'+csvPath+"?type=csv&detectTypes=yes&crs="+wgs84+"&xField=longitude&yField=latitude&spatialIndex=no&subsetIndex=no"
    csvLayer = QgsVectorLayer(uri, 'GpsLocations', 'delimitedtext')
    
    # openstreetmap layer
    tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'
    osmLayer = QgsRasterLayer(tms,'OSM', 'wms')

    project.addMapLayer(osmLayer)
    project.addMapLayer(csvLayer)
    
    csvSymbols = csvLayer.renderer().symbol()
    csvSymbols.setColor(QColor('red'))
    csvLayer.triggerRepaint()

    options = QgsMapSettings()
    options.setLayers([csvLayer,osmLayer])
    options.setBackgroundColor(QColor("transparent"))
    options.setOutputSize(QSize(3840, 2160))
    options.setExtent(csvLayer.extent())
    options.setDestinationCrs(QgsCoordinateReferenceSystem(wgs84))

    render = QgsMapRendererParallelJob(options)
    image_location = './file.png'
    render.start()
    render.waitForFinished()
    img = render.renderedImage()
    img.save(image_location, 'png')
    
    print('Map has been rendered to: ' + image_location)
    project.write("project.qgz")

    qgs.exitQgis()
    print("Exiting")
