#!/usr/bin/python3

from sys import argv

print("latitude,longitude,time")
row = list()
with open(argv[1], "r") as f:
    for line in f:
        if "lat=" in line:
            tokens = line.split("\"")
            row.append(float(tokens[1]))
            row.append(float(tokens[3]))
        if "<time>" in line:
            if len(row) == 2:
                row.append(line.split(">")[1].split("<")[0])
                print(str(row)[1:-1])
                row = list()



