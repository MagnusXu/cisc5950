# README
### Dataset
The dataset used in question2 is the original one from NYC open data website. The sub-dataset is the subset of original one, which only includes 1844 objects, which satisfy the requirement of the question.
To get the sub-dataset, go to the source website, use filter function to pick those data. You need two filters to get the same dataset I use, which are:
- The street number is in between W 53th Street to W 74th Street.
- The avenue should be one of these: Amsterdam Ave, West End Ave, Columbus Ave, Central Park West

### How to Run
I deploy everything on docker due to the reason I cannot deploy the Hadoop environment from your Github files and other problems I met on Google Cloud.

To run the script, you need to download the code, and move it to the directory you want. Then modify test.sh and run, which looks like:
```
#!/bin/sh
../../start.sh
/usr/local/hadoop/bin/hdfs dfs -rm -r /wordcount/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r /wordcount/output/
/usr/local/hadoop/bin/hdfs dfs -mkdir -p /wordcount/input/
/usr/local/hadoop/bin/hdfs dfs -copyFromLocal ../../mapreduce-test-data/test.txt /wordcount/input/
/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
-file ../../mapreduce-test-python/wordcount/mapper.py -mapper ../../mapreduce-test-python/wordcount/mapper.py \
-file ../../mapreduce-test-python/wordcount/reducer.py -reducer ../../mapreduce-test-python/wordcount/reducer.py \
-input /wordcount/input/* -output /wordcount/output/
/usr/local/hadoop/bin/hdfs dfs -cat /wordcount/output/part-00000
/usr/local/hadoop/bin/hdfs dfs -rm -r /wordcount/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r /wordcount/output/
../../stop.sh
```
