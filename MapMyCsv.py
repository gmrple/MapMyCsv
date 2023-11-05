#!/usr/bin/python3

import yaml
from sys import argv

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from qgis.core import QgsApplication, QgsProject, QgsCoordinateReferenceSystem, QgsVectorLayer, QgsRasterLayer, QgsMapSettings, QgsMapRendererParallelJob

# this should be platorm indepentent - will do windows testing later

if len(argv) > 1:
    config_path = argv[1]
    with open(config_path, "r") as f:
        config     = yaml.safe_load(f)
        projectCrs = config['settings']['projectCrs']
        csvPath    = config['settings']['csvPath']
        prefixPath = config['settings']['prefixPath']

        QgsApplication.setPrefixPath(prefixPath, True)
        qgs = QgsApplication([], False)

        qgs.initQgis()
        WGS84="EPSG:4326"

        project = QgsProject.instance()
        project.setCrs(QgsCoordinateReferenceSystem(projectCrs))

        # if you get a file imported as you want in the desktop application, you can hover over the layer
        # to gett the settings that are in the URI
        uri = 'file:///'+csvPath+"?type=csv&detectTypes=yes&crs="+WGS84+"&xField=longitude&yField=latitude&spatialIndex=no&subsetIndex=no"
        csvLayer = QgsVectorLayer(uri, 'GpsLocations', 'delimitedtext')

        # openstreetmap layer
        tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'
        osmLayer = QgsRasterLayer(tms,'OSM', 'wms')

        project.addMapLayer(osmLayer)
        project.addMapLayer(csvLayer)

        csvSymbols = csvLayer.renderer().symbol()
        csvSymbols.setColor(QColor('red'))
        csvLayer.triggerRepaint()

        # layers are done now - if you didn't care about the image, but wanted a project with
        # the defined layers you could skip to project.write() and open the resulting file

        # generate an image
        options = QgsMapSettings()
        options.setLayers([csvLayer,osmLayer])
        options.setBackgroundColor(QColor("transparent"))
        options.setOutputSize(QSize(3840, 2160))
        options.setExtent(csvLayer.extent())
        options.setDestinationCrs(QgsCoordinateReferenceSystem(WGS84))

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
