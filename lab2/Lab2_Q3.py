#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from pyspark import SparkContext, SparkConf
import sys
from operator import add
from pyspark.sql import SparkSession
import math


def get_distance(coords1, coords2):
    Sum = 0
    for i in range(len(coords1)):
        Sum += (coords1[i] - coords2[i]) ** 2
    dist = math.sqrt(Sum)
    return dist

def get_nearest_cluster(coords):
    nearest_cluster_id = None
    nearest_distance = 100000000
    for cluster in clusters:
        dist = get_distance(cluster[1:], coords)
        if dist < nearest_distance:
            nearest_cluster_id = cluster[0]
            nearest_distance = dist
    return nearest_cluster_id


def list_add(list1,list2):
    return [(list1[i]+list2[i]) for i in range(len(list1))]


reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: Lab2_Q2.py <file>", file=sys.stderr)
        sys.exit(-1)
    # create SparkContext object
    conf = SparkConf().setAppName('Lab2_Q2')
    sc = SparkContext(conf=conf)
    # read a RDD from HFDS
    textfile = sc.textfile(sys.argv[1]).map(lambda line: line.split(',')).filter(lambda line:((len(line)>1) & (line[9] != "Street Code1")))
    # abstract street coordinates and vehicle color from the dataset
    data = textfile.map(lambda line: [int(line[9]),int(line[10]),int(line[11]),str(line[33])])
    streets = data.map(lambda: line: data[0:3])

    # for the the purpose of the lab, I reduced sample size to only 10000 so that we can get the results faster
    streets = data.takeSample(withReplacement=False, num=10000, seed=1)
    
    # randomly draw three coordinates for one street as initial centroids
    clusters = [["C"+ str(i+1)] + street.takeSample(withReplacement=False, num=3, seed=1)[i] for i in range(3)]
    
    niter = 0
    while niter <= 20:
        prev_clusters = clusters
        data_nearest = street.map(lambda line: line + [get_nearest_cluster(line)])
        for i in range(3):
            data_Ci = data_nearest.filter(lambda line: line[-1] == "C"+ str(i+1))
            num = data_Ci.count()
            clusters[i] = ["C"+ str(i+1)]+[((data_Ci.map(lambda line: line[0:3]).reduce(list_add))[j]/num) for j in range(3)]
        if clusters == prev_clusters:
            break
        niter = niter + 1




    data_cluster_assigned = data.map(lambda line: line + [get_nearest_cluster(line)])
    target_cluster = data_cluster_assigned.filter(lambda line: line[-1] == get_nearest_cluster([34510, 10030, 34050]))
    total_cars = target_cluster.count()
    black_cars = target_cars.filter(lambda line: (line[-2] == "BK") | (line[-2] == "BL") | (line[-2] == "BLACK")).count()

    print("The probability that a black car with the given street codes will get a ticket is:\t{}".format(
                                                                                                      black_cars / total_cars))







