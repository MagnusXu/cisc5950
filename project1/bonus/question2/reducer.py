#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import operator
import re
import numpy as np
import pandas as pd

df = pd.read_csv("/Users/MagnusXu/Desktop/subData.csv")
samples = df.shape[0]
cluster = mat(zeros((samples, 2)))
index = 0

def eud(vector1, vector2):
	return np.linalg.norm(vector1-vector2)

for line in sys.stdin:
	line = line.sprip()
	# location is the combination of three street codes, like (3, 54, 1)
	centroids, location = line.split('\t')
	minDist = 10000.0
	minIndex = 0
	# find the closet centroid
	for j in range(3): # 3 is the number of centroids
		dis = eud(centroids[j,:], location)
		if dis < minDist:
			minDist = dis
			minIndex = j
    
    # update cluster
	if cluster[index, 0] != minIndex:
		cluster[index, :] = meanIndex, minDist ** 2

    # update centroids
	for j in range(3):
		points = df[nonzero(cluster[:,0].A == j)[0]]
		centroids[j,:] = mean(points, axis = 0)

	# update the index for the next round to use
	index += 1

print(centroids)
