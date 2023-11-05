H.2 Map My CSV
Script to take a CSV containing latitude and longitude and creating a QGIS project and a image of the data mapped on OpenStreetMaps 
NOTE: The CSV file MUST have a row at the top with `latitude,longitude,etc` set in the order of the following data

used https://github.com/thehatter8/CSVMappy/blob/main/mapbuilder.py as a starting point. This works on Arch Linux as of 4 Nov 2023.

Dependencies - a working QGIS Install. Tested with QGIS 3.34

TODO:
* Add a legend with a figure noting scale
* Ensure this works on windows
* make layers configurable
