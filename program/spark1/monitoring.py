import subprocess
import requests
import time
import os
import math
import actions

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def main():

 FNULL = open(os.devnull, "w")
 
#query spark history server to obtain metrics of last submitted application 
#app id
 r1 = requests.get("http://127.0.0.1:1808"+str(actions.c_id)+"/api/v1/applications/").json()

 s=r1[0]

 id=s["id"]

# response time [s]
 r2=requests.get("http://127.0.0.1:1808"+str(actions.c_id)+"/api/v1/applications/"+str(id)).json()
 p=r2["attempts"]
 d=p[0]
 duration=d["duration"]/1000
 print("response time: "+ str(duration)+" s")
 
 #execution time [s]
 r3=requests.get("http://127.0.0.1:1808"+str(actions.c_id)+"/api/v1/applications/"+str(id)+"/executors").json()
 t=r3[0]
 ex=t["totalDuration"]/1000
 print ("execution time: "+ str(ex)+" s")

#number of records processed
 r3=requests.get("http://127.0.0.1:1808"+str(actions.c_id)+"/api/v1/applications/"+str(id)+"/stages/1").json()
 re=r3[0]
 rec=re["inputRecords"]

#throughput calculated as number of records processed /execution time [n/s]
 throughput= rec/ex
 throughput= truncate(throughput,2)
 print("throughput: "+ str(throughput)+" n/s")

 #query toxiproxy to obtain latency [ms]
 r4=requests.get("http://127.0.0.1:8474/proxies/minioProxy"+str(actions.c_id)+"/toxics/latency")
 r4=r4.json()
 latency=r4["attributes"]["latency"]
 print("Latency: "+ str(latency) +" ms")



 yield duration
 yield ex
 yield throughput
 yield latency


