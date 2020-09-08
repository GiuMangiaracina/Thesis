import pyspark
sc = pyspark.SparkContext(appName="cholesterol_AVG_Application");
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
multiline_df = sqlContext.read.option("multiline","true").json("s3a://miniobucket/file1.json")
multiline_df.createOrReplaceTempView("table")
sqlContext.sql("select AVG(cholesterol) from table").show()