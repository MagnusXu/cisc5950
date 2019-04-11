#!/usr/bin/env python

import sys

def gen_new_cluster(id, vals):
    s = id + "\t"
    for i in range(len(vals)-1):
        s = s + str(vals[i] / vals[-1]) + ";"
    print(s[:-1])

old_id = None
sum_vals = [0.0 for i in range(4)]
for line in sys.stdin:
    id, data = line.strip().split("\t")
    vals = data.strip().split(";")
    vals = [float(x) for x in vals]
    if old_id and old_id != id:
        gen_new_cluster(old_id, sum_vals)
        sum_vals = [0.0 for i in range(4)]
    old_id = id
    sum_vals = [sum_vals[i] + vals[i] for i in range(4)]

if old_id:
    gen_new_cluster(old_id, sum_vals)
