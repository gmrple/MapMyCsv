# Map My CSV
Script to take a CSV containing latitude and longitude and creating a QGIS project and a image of the data mapped on OpenStreetMaps 
NOTE: The CSV file MUST have a row at the top with `latitude,longitude,etc` set in the order of the following data

used https://github.com/thehatter8/CSVMappy/blob/main/mapbuilder.py as a starting point. This works on Arch Linux as of 4 Nov 2023.

Dependencies - a working QGIS Install. Tested with QGIS 3.34 on Arch Linux and 3.28 on Windows 11

## How To
1. Update the paths in map.bash or map.bat to match your QGIS install and version
2. modify a config file (see the config folder) to specify the CSVs you want mapped
3. run map.bash or map.bat if you are on Linux or Windows respectively
4. check out file.png and project.qgz

## TODO
* Add a legend with a figure noting scale
* ~~Ensure this works on windows~~ Done!
* ~~make layers configurable~~ you can now add multiple layers
* ~~handle determining output map extent based on all of the layers~~ Rendered image is set based on the space occupied by all csv layers
