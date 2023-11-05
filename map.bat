@echo off
REM Update this script to work for your environment
REM See the PyQgis Cookbook Introduction section for guidance
REM for 3.28 https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/intro.html
set PATH=C:\Program Files\QGIS 3.28.12\bin;C:\Program Files\QGIS 3.28.12\apps\qgis-ltr\bin;%PATH%

REM This must be set, thanks Giovanni Gallon https://medium.com/@giovannigallon/how-i-automate-qgis-tasks-using-python-54df35d8d63f
set PATH=C:\Program Files\QGIS 3.28.12\apps\Qt5\bin;%PATH%

REM this wasn't clearly documented... PYTHONHOME should be the actually python installation
REM PYTHONPATH is the serach path for the QGIS python modules
set PYTHONPATH=C:\Program Files\QGIS 3.28.12\apps\qgis-ltr\python
set PYTHONHOME=C:\Program Files\QGIS 3.28.12\apps\Python39

python MapMyCsv.py config/config-windows.yaml