#!/usr/bin/python3

"""Simple script to grab lat and long from a gpx file. You can get them from
many work out trackers, for example Garmin bike computers. This is what
I used to generate my test csvs
"""

from sys import argv

OFFSET = True

print("latitude,longitude,time")
row = []
with open(argv[1], "r", encoding="UTF-8") as f:
    for line in f:
        if "lat=" in line:
            tokens = line.split("\"")
            latitude  = float(tokens[1])
            longitude = float(tokens[3])
            if OFFSET:
                latitude = latitude + 0.01
            row.append(latitude)
            row.append(longitude)
        if "<time>" in line:
            if len(row) == 2:
                row.append(line.split(">")[1].split("<")[0])
                # I love this trick to make lists into CSV,
                # the str() function does all the work
                print(str(row)[1:-1])
                row = []
