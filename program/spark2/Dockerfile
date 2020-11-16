FROM gettyimages/spark

#copy script
COPY . /$SPARK_HOME/bin/ 
COPY spark-defaults.conf /$SPARK_HOME/conf 
COPY log4j.properties.conf /$SPARK_HOME/conf



#set minio credentials
ENV AWS_ACCESS_KEY_ID="minio"
ENV AWS_SECRET_ACCESS_KEY="minio123"

RUN pip install numpy && pip install findspark && pip install requests && pip install pymysql && mkdir -p /tmp/spark-events  && apt-get update && apt-get install nano && pip install termcolor  && chmod 777 -R ./

CMD /bin/bash && cd /$SPARK_HOME/sbin 
    

WORKDIR $SPARK_HOME/bin



