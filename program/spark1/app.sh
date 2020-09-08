#!/bin/bash
{ time spark-submit --master local[2] --conf spark.hadoop.fs.s3a.endpoint=http://127.0.0.1:8000 script.py 2>1 ;} 2>> time.log