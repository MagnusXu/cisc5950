#!/usr/bin/env python

import sys, math

CLUSTERS_FILENAME = sys.argv[1]
NEW_CLUSTERS_FILENAME = sys.argv[2]

def cal_distance(coords1, coords2):
    #Calculate euclidian distance between two sets of coordinates
    sum = 0
    for i in range(len(coords1)):
        sum += (coords1[i] - coords2[i]) ** 2
    dist = math.sqrt(sum)
    return dist

clusters1 = []
f = open(CLUSTERS_FILENAME, 'r')
cluster_data = f.read()
f.close()
for line in cluster_data.strip().split("\n"):
    id, data = line.strip().split(":")
    coords = data.strip().split(";")
    coords = [float(x) for x in coords]
    clusters1.append(coords)

clusters2 = []
f = open(NEW_CLUSTERS_FILENAME, 'r')
cluster_data = f.read()
f.close()
for line in cluster_data.strip().split("\n"):
    id, data = line.strip().split("\t")
    coords = data.strip().split(";")
    coords = [float(x) for x in coords]
    clusters2.append(coords)

total_dist = 0
for i in range(len(clusters1)):
    dist = cal_distance(clusters1[i], clusters2[i])
    total_dist += dist

print(total_dist)
