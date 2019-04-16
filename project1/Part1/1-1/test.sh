#!/bin/sh

mvn clean package
/usr/local/hadoop/bin/hdfs dfs -rm -r /proj1-1/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r /proj1-1/output/
/usr/local/hadoop/bin/hdfs dfs -mkdir -p /proj1-1/input/
/usr/local/hadoop/bin/hdfs dfs -copyFromLocal 
/project1/Parking_Violations_Issued_-_Fiscal_Year_2019.csv 
/proj1-1/input/
/usr/local/hadoop/bin/hadoop jar 
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
-file /project1/1-1/mapper.py -mapper /project1/1-1/mapper.py \
-file /project1/1-1/reducer.py -reducer /project1/1-1/reducer.py \
-input /proj1-1/input/* -output /proj1-1/output/
/usr/local/hadoop/bin/hdfs dfs -cat /proj1-1/output/part-00000
/usr/local/hadoop/bin/hdfs dfs -rm -r /proj1-1/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r /proj1-1/output/
mvn clean

