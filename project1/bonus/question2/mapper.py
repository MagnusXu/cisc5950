#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import operator
import re
from numpy import *
import pandas as pd

reg = reg.compile('5[3-9]|6[0-9]|7[0-4]')

df = pd.read_csv("/Users/MagnusXu/Desktop/subData.csv")

# Init of Centroids with Samples
samples, dimension = df.shape
centroids = zeros((3, dimension))
for i in range(3):
	index = int(random.uniform(0, samples))
	centroids[i,:] = df[index,:]

for line in sys.stdin:
	line = line.split(',')
	match1 = (line[25]=='Amsterdam Ave'|'West End Ave'|'Columbus Ave'|'Central Park West')
	match2 = (line[26]=='Amsterdam Ave'|'West End Ave'|'Columbus Ave'|'Central Park West')
	if (match1 or match2):
		match3 = reg.search(line[25])
		match4 = reg.search(line[26])
		if (match3 or match4):
			stCode1 = line['Street Code1']
			stCode2 = line['Street Code2']
			stCode3 = line['Street Code3']
			print('%s\t%s' % (centroids[0] + '|' + centroids[1] + '|' + centroids[2], streetcode1 + '|' + streetcode2 + '|'+streetcode3)

