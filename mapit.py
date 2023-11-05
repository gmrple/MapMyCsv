#!/usr/bin/python3

import yaml
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from qgis.core import *

with open("./MapMyCsv.yaml", "r") as f:
    print("opened config file")
    config = yaml.safe_load(f)
    elipsoid = config['settings']['elipsoid']
    csvPath = config['settings']['csvPath']
    crsId = int(elipsoid.split(":")[1])
    
    # Initiate Application
    QgsApplication.setPrefixPath("/usr/bin/qgis", True)
    print("set prefix")
    qgs = QgsApplication([], False)
    
    qgs.initQgis()
    print("Application initiated")

    # Start project instance
    project = QgsProject.instance()
    #project.setCrs(QgsCoordinateReferenceSystem(crsId))

    # Build layer from CSV and check validity
    uri = 'file://' + csvPath +'?delimiter={}&xField={}&yField={}&crs={}'.format(',', 'longitude', 'latitude',{'epsg:4326'})
    print(uri)
    csvLayer = QgsVectorLayer(uri, 'Locations', 'delimitedtext')

    tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'
    osmLayer = QgsRasterLayer(tms,'OSM', 'wms')

    if csvLayer.isValid():
        print('CSV Layer successfully imported')
    else:
        print('CSV Import failed')
    if osmLayer.isValid:
        print('OpenStreetMaps layer imported')
    else:
        print('unable to make OpenStreetMaps Layer')
        sys.exit(0)


    # Adding map layers
    project.addMapLayer(osmLayer)
    project.addMapLayer(csvLayer)

    # Set layer colors and create some outlines
    csvSymbols = csvLayer.renderer().symbol()
    csvSymbols.setColor(QColor('red'))
    csvLayer.triggerRepaint()

    # Set layer order and output options
    options = QgsMapSettings()
    options.setLayers([osmLayer,csvLayer])
    options.setBackgroundColor(QColor("transparent"))
    options.setOutputSize(QSize(3840, 2160))
    options.setExtent(csvLayer.extent())

    mapLayers = project.mapLayers()
    for x, y in enumerate(mapLayers): print('Layer ' + str(x+1) + ': '+ str(y.split('_')[0]))

    # Start image render

    render = QgsMapRendererParallelJob(options)
    image_location = './file.png'
    render.start()
    render.waitForFinished()
    img = render.renderedImage()
    img.save(image_location, 'png')
    print('Map has been rendered to: ' + image_location)


    # End of project code
    qgs.exitQgis()
    print("Exiting")
