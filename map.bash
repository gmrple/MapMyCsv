#!/bin/bash

# Update this script to work for your environment
# See the PyQgis Cookbook Introduction section for guidance
# for 3.28 https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/intro.html

# sets environment needed to run in archlinux 4 NOV 2023
export PYTHONPATYH=/usr/share/qgis/python
./MapMyCsv.py config/config-linux.yaml
