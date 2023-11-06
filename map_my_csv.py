#!/usr/bin/python3

"""Creates an image and a QGIS project from one or multile CSVs
     Should be called from map.bash or map.bat, ir you are on
     linux or windows respectively. Two arguments are passed
     from the outer script, the location of the QGIS intall,
     and a YAML file specifying what CSV files to process and
     what color should be used for each dataset
"""

import sys
from os.path      import basename
import yaml

from PyQt5.QtCore import QSize
from PyQt5.QtGui  import QColor
from qgis.core    import QgsApplication, QgsProject,                           \
        QgsCoordinateReferenceSystem, QgsVectorLayer, QgsRasterLayer,          \
        QgsMapSettings, QgsMapRendererParallelJob, QgsRectangle,               \
        QgsLayoutItemMap, QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes,         \
        QgsPrintLayout, QgsLayoutItemLabel, QgsLayoutExporter,                 \
        QgsLayoutItemLegend, QgsLayoutItemScaleBar

# this is platform indepentent - will do Mac OS testing later, works on Windows and Linux

#constants
WGS84="EPSG:4326"

# read command line args and config
if len(sys.argv) > 2:
    PREFIX      = sys.argv[1]
    config_path = sys.argv[2]
    with open(config_path, "r", encoding="UTF-8") as f:
        try:
            config     = yaml.safe_load(f)
            projectCrs = config['project']['crs']
            csvFiles   = config['project']['layers']

            # sanity check the specification
            for csvFile in csvFiles:
                if "csvPath" not in csvFile:
                    print("missing required field, csvPath")
                    sys.exit(1)
                if "crs" not in csvFile:
                    csvFile['crs'] = WGS84
                if "color" not in csvFile:
                    print("missing required field, color")
                    sys.exit(1)

        except LookupError as e:
            print("invalid configuration - exiting" + str(e))
            print(config)
            sys.exit(1)

        f.close()

        # start the QGIS instance
        QgsApplication.setPrefixPath(PREFIX, True)
        qgs = QgsApplication([], False)
        qgs.initQgis()

        project = QgsProject.instance()
        project.setCrs(QgsCoordinateReferenceSystem(projectCrs))

        # openstreetmap layer
        TMS = 'type=xyz&url=https://tile.openstreetmap.org/' \
            + '{z}/{x}/{y}.png&zmax=19&zmin=0'
        osmLayer = QgsRasterLayer(TMS,'OSM', 'wms')
        project.addMapLayer(osmLayer)

        allLayers = []

        # create layers for each CSV file
        for csvFile in csvFiles:
            csvPath = csvFile['csvPath']
            crs     = csvFile['crs']
            color   = csvFile['color']

            # if you get a file imported as you want in the desktop application
            # you can hover over the layer # to gett the settings that are in
            # the URI
            uri = 'file:///'+csvPath                      \
                    + "?type=csv&detectTypes=yes&crs="    \
                    + crs                                 \
                    + "&xField=longitude&yField=latitude" \
                    + "&spatialIndex=no&subsetIndex=no"
            csvLayer = QgsVectorLayer(uri, basename(csvPath), 'delimitedtext')

            if not csvLayer.isValid():
                print("invailid layer: " + csvPath)
                sys.exit(1)

            project.addMapLayer(csvLayer)

            csvSymbols = csvLayer.renderer().symbol()
            csvSymbols.setColor(QColor(color))
            csvLayer.triggerRepaint()
            allLayers.insert(0,csvLayer)
        
        # define a rectangle that all the data fits in
        extent = allLayers[0].extent()
        xmax = extent.xMaximum()
        xmin = extent.xMinimum()
        ymax = extent.yMaximum()
        ymin = extent.yMinimum()
        for layer in allLayers:
            extent = layer.extent()
            if extent.xMinimum() < xmin:
                xmin = extent.xMinimum()
            if extent.xMaximum() > xmax:
                xmin = extent.xMaximum()
            if extent.yMinimum() < ymin:
                ymin = extent.yMinimum()
            if extent.yMaximum() > ymax:
                ymin = extent.yMaximum()

        rect = QgsRectangle(xmin, ymin, xmax, ymax)
        rect.scale(1.1) # zoom out a bit for context
        allLayers.append(osmLayer)

        # layers are done now - if you didn't care about the image, but wanted
        # a project with the defined layers you could skip to project.write()
        # and open the resulting file

        # generate an image
        options = QgsMapSettings()
        options.setLayers(allLayers)
        options.setBackgroundColor(QColor("transparent"))
        options.setOutputSize(QSize(3840, 2160))
        options.setExtent(rect)
        options.setDestinationCrs(QgsCoordinateReferenceSystem(WGS84))

        render = QgsMapRendererParallelJob(options)
        IMAGE_LOCATION= './file.png'
        render.start()
        render.waitForFinished()
        img = render.renderedImage()
        img.save(IMAGE_LOCATION, 'png')

        print('Map has been rendered to: ' + IMAGE_LOCATION)

        # Create a layout based output
        layout = QgsPrintLayout(project)
        layout.initializeDefaults()
        layout.setName("GeneratedLayout")
        project.layoutManager().addLayout(layout)
        
        # elements in the layout
        theMap = QgsLayoutItemMap(layout)
        # example resizes here... not sure that's something I want
        theMap.attemptMove(QgsLayoutPoint(5,5, QgsUnitTypes.LayoutMillimeters))
        theMap.attemptResize(QgsLayoutSize(200,200, QgsUnitTypes.LayoutMillimeters))

        theMap.zoomToExtent(rect)
        layout.addItem(theMap)

        # Retrieve width & height values of map item
        map_item = [i for i in layout.items() if isinstance(i, QgsLayoutItemMap)][0]
        map_width = map_item.sizeWithUnits().width()
        map_height = map_item.sizeWithUnits().height()
        
        legend = QgsLayoutItemLegend(layout)
        legend.setLinkedMap(theMap)
        layout.addLayoutItem(legend)

        scaleBar = QgsLayoutItemScaleBar(layout)
        scaleBar.setStyle("Double Box")
        scaleBar.setLinkedMap(theMap)
        scaleBar.applyDefaultSize()
        layout.addLayoutItem(scaleBar)
        legend.attemptMove(QgsLayoutPoint(map_width-30, map_height-20, QgsUnitTypes.LayoutMillimeters), useReferencePoint=True)

        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf("./demo.pdf", QgsLayoutExporter.PdfExportSettings())

        project.write("project.qgz")
        qgs.exitQgis()
        print("Exiting")
