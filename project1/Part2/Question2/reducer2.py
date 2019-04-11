#!/usr/bin/env python

import sys
from operator import itemgetter

dict_player = {}
for line in sys.stdin:
    dict_cluster = {}
    line = line.strip()
    player, cluster, made = line.split('\t')
    made = int(made)
    if player not in dict_player:
        dict_cluster[cluster] = [made, 1.0]
        dict_player[player] = dict_cluster
    else:
        dict_cluster = dict_player[player]
        val = dict_cluster.get(cluster, [0, 0.0])
        dict_cluster[cluster] = [val[0] + made, val[1] + 1]
        dict_player[player] = dict_cluster

for i in dict_player:
    for j in dict_player[i]:
        dict_player[i][j] = dict_player[i][j][0] / dict_player[i][j][1]
    try:
        sorted_cluster_rate = sorted(dict_player[i].items(), key=itemgetter(1))[::-1]
        for cluster, hit_rate in sorted_cluster_rate:
            print('%s\t%s\t%.2f' % (i, cluster, hit_rate))
    except:
        pass
