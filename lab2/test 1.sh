#!/bin/bash

source /spark-examples/env.sh

/spark-examples/start.sh
/usr/local/hadoop/bin/hdfs dfs -rm -r /Lab2_Q2/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r /Lab2_Q2/output/
/usr/local/hadoop/bin/hdfs dfs -mkdir -p /Lab2_Q2/input/
/usr/local/hadoop/bin/hdfs dfs -copyFromLocal ../../test-data/Parking_Violations_Issued_-_Fiscal_Year_2019.csv /Lab2_Q2/input/
/usr/local/spark/bin/spark-submit --master=spark://$SPARK_MASTER:7077 /Lab2_Q2/Lab2_Q2.py hdfs://$SPARK_MASTER:9000/Lab2_Q2/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r /Lab2_Q2/input/
/spark-examples/stop.sh
