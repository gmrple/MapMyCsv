#!/usr/bin/python3

from sys import argv

# Simple script to grab lat and long from a gpx file. You can get them from
# many work out trackers, for example Garmin bike computers. This is what 
# I used to generate my test csvs

offset = True

print("latitude,longitude,time")
row = list()
with open(argv[1], "r") as f:
    for line in f:
        if "lat=" in line:
            tokens = line.split("\"")
            latitude  = float(tokens[1])
            longitude = float(tokens[3])
            if (offset)
                latitude = latitude + 0.0001
            row.append(latitude)
            row.append(longitude)
        if "<time>" in line:
            if len(row) == 2:
                row.append(line.split(">")[1].split("<")[0])
                # I love this trick to make lists into CSV, 
                # the str() function does all the work
                print(str(row)[1:-1])
                row = list()



