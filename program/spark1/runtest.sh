#!/bin/bash
echo 'TEST RESULTS \n' >> time.log
for (( i = 0 ; i < 10; i++ )) do
{ spark-submit --master local[2] --conf spark.hadoop.fs.s3a.endpoint=http://192.168.99.100:8000 script.py 2>1 ;} 2>> time.log
done