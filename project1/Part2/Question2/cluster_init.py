#!/usr/bin/python

import sys, csv

DATA_FILENAME = sys.argv[1]
CLUSTERS_FILENAME = sys.argv[2]

def validate_data(coords):
    if coords[0] == 'SHOT_DIST':
        return False
    for x in coords:
        if x == "":
            return False
        elif float(x) < 0:
            return False
    return True

count = 0
f = open(CLUSTERS_FILENAME, 'w')
with open(DATA_FILENAME) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for line in readCSV:
        if count >= 4:
            break
        coords = [line[11], line[16], line[8]]
        if not validate_data(coords):
            continue
        coords = [float(x) for x in coords]

        count += 1
        s = "C" + str(count) + "\t"
        for i in range(len(coords)):
            s = s + str(coords[i]) + ";"
        f.write(s[:-1] + "\n")

f.close()
del f
