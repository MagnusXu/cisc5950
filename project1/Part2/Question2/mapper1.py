#!/usr/bin/env python

import sys, math, os

clusters_data = str(os.environ['clusters_data'])

clusters = []
delta_clusters = dict()

def read_clusters():
    for line in clusters_data[:-1].strip().split("|"):
        id, data = line.strip().split(":")
        coords = data.strip().split(";")
        coords = [float(x) for x in coords]
        clusters.append([id] + coords)
        delta_clusters[id] = [0 for i in range(len(coords)+1)]

def cal_distance(coords1, coords2):
    #Calculate euclidian distance between two sets of coordinates
    sum = 0
    for i in range(len(coords1)):
        sum += (coords1[i] - coords2[i]) ** 2
    dist = math.sqrt(sum)
    return dist

def get_nearest_cluster(coords):
    nearest_cluster_id = None
    nearest_distance = 10000000
    for cluster in clusters:
        dist = cal_distance(cluster[1:], coords)
        if dist < nearest_distance:
            nearest_cluster_id = cluster[0]
            nearest_distance = dist
    return nearest_cluster_id

def validate_data(coords):
    if coords[0] == 'PTS_TYPE':
        return False
    for x in coords:
        if x == "":
            return False
        elif float(x) < 0:
            return False
    return True

read_clusters()

for line in sys.stdin:
    columns = line.strip().split(",")
    coords = [columns[12], columns[18], columns[9]]
    if not validate_data(coords):
        continue
    coords = [float(x) for x in coords]
    nearest_cluster_id = get_nearest_cluster(coords)
    vals = delta_clusters[nearest_cluster_id]
    vals[-1] += 1
    vals[:-1] = [vals[i] + coords[i] for i in range(len(coords))]
    delta_clusters[nearest_cluster_id] = vals

for key in delta_clusters:
    s = key + "\t"
    for v in delta_clusters[key]:
        s = s + str(v) + ";"
    print(s[:-1])
