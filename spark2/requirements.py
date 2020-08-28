import json
def main():
 with open('goal.json','r') as jsonfile:
    json_content = json.load(jsonfile)
   
 json_content["initialized"] = 1
   
 r = int(input ("\n"+"Enter max Response time Threshold in seconds:"))   
   
 json_content["maxValueRT"] = r

 l = int(input ("\n"+"Enter max Latency Threshold in milliseconds:"))   
   
 json_content["maxValueNL"] = l


 t = int(input ("\n"+"Enter min Throughput Threshold:"))   
   
 json_content["minValueX"] = t

 e = int(input ("\n"+"Enter max execution time Threshold in seconds:"))   
   
 json_content["maxValueET"] = e

 a = int(input ("\n"+"Enter min Availability Threshold :"))   
   
 json_content["minValueA"] = a

 with open('goal.json','w') as jsonfile:
    json.dump(json_content, jsonfile, indent=4)
 