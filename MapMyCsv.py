#!/usr/bin/python3

import yaml
from sys import argv, exit

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from qgis.core import QgsApplication, QgsProject, QgsCoordinateReferenceSystem, QgsVectorLayer, QgsRasterLayer, QgsMapSettings, QgsMapRendererParallelJob

# this should be platorm indepentent - will do windows testing later

WGS84="EPSG:4326"
if len(argv) > 2:
    prefix      = argv[1]
    config_path = argv[2]
    with open(config_path, "r") as f:
        try:
            config     = yaml.safe_load(f)
            projectCrs = config['project']['crs']
            layers     = config['project']['layers']

            # sanity check the specification 
            for layer in layers:
                if "csvPath" not in layer:
                    print("missing required field, csvPath")
                    exit(1)
                if "crs" not in layer:
                    layer['crs'] = WGS84
                if "color" not in layer:
                    print("missing required field, color")
                    exit(1)

        except Exception as e:
            print("invalid configuration - exiting" + str(e))
            print(config)
            exit(1)

        QgsApplication.setPrefixPath(prefix, True)
        qgs = QgsApplication([], False)

        qgs.initQgis()

        project = QgsProject.instance()
        project.setCrs(QgsCoordinateReferenceSystem(projectCrs))

        # openstreetmap layer
        tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'
        osmLayer = QgsRasterLayer(tms,'OSM', 'wms')
        project.addMapLayer(osmLayer)

        allLayers = [osmLayer]
        for layer in layers:
            csvPath = layer['csvPath']
            crs     = layer['crs']
            color   = layer['color']

            # if you get a file imported as you want in the desktop application, you can hover over the layer
            # to gett the settings that are in the URI
            uri = 'file:///'+csvPath+"?type=csv&detectTypes=yes&crs="+crs+"&xField=longitude&yField=latitude&spatialIndex=no&subsetIndex=no"
            csvLayer = QgsVectorLayer(uri, 'GpsLocations', 'delimitedtext')
            project.addMapLayer(csvLayer)

            csvSymbols = csvLayer.renderer().symbol()
            csvSymbols.setColor(QColor(color))
            csvLayer.triggerRepaint()
            allLayers.insert(0,csvLayer)

        # layers are done now - if you didn't care about the image, but wanted a project with
        # the defined layers you could skip to project.write() and open the resulting file

        # generate an image
        options = QgsMapSettings()
        options.setLayers(allLayers)
        options.setBackgroundColor(QColor("transparent"))
        options.setOutputSize(QSize(3840, 2160))
        options.setExtent(allLayers[0].extent())
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
