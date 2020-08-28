import subprocess
import os
import time
import json
import math
import numpy as np
import random

LEARNING_RATE = 0.2
EPISODES = 100
max_val= 0
min_val= 0
Q_table= []

# metric class
class Metric:
  def __init__(self,name,min,max,weight,status):
    self.name = name
    self.min = min
    self.max = max
    self.weight = weight
    self.status = status


# action class
class Action:

  def __init__(self,id, description, delay,s):
    self.id = id
    self.description = description
    self.delay = delay
    self.s=s
#actions for node 2
A0 = Action(0, "node 0", 1300,0)
A1 = Action(1, "node 1", 750,0)
A2 = Action(2, "local copy", 0,0)
A3 = Action(3, "node 3", 2000,0)

action_list =[A0,A1,A2,A3]
class Environment:
  def __init__(self, n):
    
    #number of vdc
    self.n = n
    
  def step(self,action):
    print("Retrieve data from : " + action.description)
    
    modify(action.delay)
    elapsed_time = training_computation()
    
    #reward assigment
    if elapsed_time < max_val:
      print("\n"+"Goal not violated")
      reward = 1
      action.s +=1
    else :
        print("\n"+"Goal violated")
        reward = -1

    return reward

def main():
 
 with open('goal.json','r') as jsonfile:
    json_content = json.load(jsonfile)
 if json_content['initialized'] == 0:
    init()
 else :
    pass
 computation()

def computation() :
 global Q_table 
 n = int(input ("Enter number of computations: "))
 FNULL = open(os.devnull, "w")
 with open('goal.json','r') as jsonfile:
    json_content0 = json.load(jsonfile)   
 val = json_content0["maxValue"]
 print("\n"+"Goal-> "+"(min: "+str(json_content0["minValue"]) +" - max: "+ str(val)+") seconds")
 sum=0;
 i=0;
 f = open("time.log", "a")
 f.write("\n"+"Test Results :"+"\n")
 f.close()

 Q_table = np.loadtxt("q_table.txt")
 print ("read Q-TABLE:")
 print(Q_table)
 for x in range (0,n):
  print("\n"+"Computation started ")
  start_time = time.time()
  subprocess.call(["./app.sh"], stdout=FNULL, stderr=subprocess.STDOUT)
  elapsed_time = time.time() - start_time
  elapsed_time= truncate(elapsed_time,3)
  print("\n")
  print("\n"+"Computation finished in :" + str(elapsed_time) + " seconds ")
  sum=sum+elapsed_time
  if elapsed_time < val:
     print("\n"+"Goal not violated")
     
  else :
     print("\n"+"Goal violated")
     repair()
     
 if  n > 1 :
     print("\n"+"computations finished. ")
     mean=sum/n
     print("\n"+"Average Time: "+ str(mean))
#write mean time in text file
     f = open("time.log", "a")
     f.write("\n"+"Average Time :" + str(mean))
     f.close()
 else:
     pass
    

def init():
 print("Initializing")
 global max_val
 global min_val
 #add proxy
 subprocess.call(["./addProxy.sh"])
 print("\n"+"\n"+"Proxy added")
 n=0
 with open('template.json','r') as jsonfile:
    json_content = json.load(jsonfile)
    
    json_content["attributes"]["latency"] = n

 with open('template.json','w') as jsonfile:
    json.dump(json_content, jsonfile, indent=4)

 subprocess.call(["./set.sh"])
 t = int(input ("\n"+"Enter max Response time Threshold in seconds:"))
 #set response time thresholds
 with open('goal.json','r') as jsonfile:
    json_content = json.load(jsonfile)
 min = json_content["minValue"]
 val_min = min
 while t < min :  
    print("Max Response time threshold lower than the minimum time required to the computation. Please insert a valid Threshold")  
    t = int(input ())
 max_val = t
 json_content["maxValue"] = t
 json_content["initialized"] = 1
 with open('goal.json','w') as jsonfile:
    json.dump(json_content, jsonfile, indent=4)
 #start training   
 training()
 l = int(input ("\n"+"set initial latency: "+"\n"))
 modify(l)
    
    
def modify(n):
 with open('template.json','r') as jsonfile:
    json_content = json.load(jsonfile)
    json_content["attributes"]["latency"] = n
 
 with open('template.json','w') as jsonfile:
    json.dump(json_content, jsonfile, indent=4)
 subprocess.call(["./modify.sh"])


def repair() :
 

 id = np.argmax(Q_table)
 for a in action_list:
       if a.id == id:
          selected_action= a
       else :
           pass
 print("\n"+"Repair action enacted.(move/copy/retrieve from a copy in another node) A"+ str(selected_action.id))          
 print("Retrieve data from : " + selected_action.description)
 modify(selected_action.delay)
    
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def training():
 #environment with 3 vdc

 env = Environment(3)
 counter=0 
    #instantiate response time-> taken from individual goal
 I1 = Metric("response_time", min_val, max_val, 1, 0)
 metrics=[I1.status]

 metrics_number=len(metrics)
    # 4 actions = number of nodes
 c0=0
 c1=0
 c2=0
 c3=0
  #delays

 available_action_list = []
 action_number= len(action_list)

 print("Training started.") 
  #initialize q_table with zeros (or random variables)
 #q_table=np.random.uniform(low=-1, high=0, size=( action_number, metrics_number))
 q_table= np.zeros((action_number,metrics_number))
 print("Initial Q-table")
 print(q_table)
 
 number=[0,1,2,3]

 n=int(round(EPISODES//action_number))

 r=EPISODES % action_number
 
 array=[]
 
 for i in number:
   v=[]
   v=[i]*n
   array=np.append(array,v)

 i=1
 if r!=0:
  for i in range(r):
    
       array=np.append(array,-1)
 
 else:
    pass
 
 np.random.shuffle(array)

 #repeat the same random sequence
 #np.random.seed(5)     
 for episode in range(EPISODES):
    counter=counter+1
    
    #id = np.random.randint(0, action_number)
    
    print("episode number:"+str(counter)+"/"+str(EPISODES))
    #id= np.random.choice(number)
    id= int(round(array[counter-1]))
    if id==0:
       c0 += 1
    
    elif id==1:
         c1 += 1

    elif id==2:
         c2 += 1

    elif id ==3:
        c3 += 1
    else: 
         pass
    
    

    for a in action_list:
       if a.id == id :
          selected_action= a
     
          reward = env.step(selected_action)
    
          print ("obtained Reward : "+ str(reward))
          print("Action A" + str(id)+" performed.")
          current_q = q_table[selected_action.id]
          print ("old q-value:\n")
          print(current_q)

    # Q- Learning update rule (modified)
          new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * reward
          print ("new q-value:\n")
          print(new_q)
          print("Updated Q-table:")
          q_table[selected_action.id] = new_q
          print(q_table)
       else:
          pass     



 print("Training finished.") 
 np.savetxt("q_table.txt", q_table)    
 print("Count of outcomes-> 0:"+ str(c0)+" /1:"+str(c1)+" /2:"+str(c2)+" /3:"+str(c3))
 print("Probability of success for action-> A0:"+ str(A0.s/c0)+" /A1:"+str(A1.s/c1)+" /A2:"+str(A2.s/c2)+" /A3:"+str(A3.s/c3))
 
def training_computation():
 FNULL = open(os.devnull, "w")
 print("max value:"+ str(max_val))
 print("\n"+"Computation started ")
 start_time = time.time()
 subprocess.call(["./app.sh"], stdout=FNULL, stderr=subprocess.STDOUT)
 elapsed_time = time.time() - start_time
 elapsed_time= truncate(elapsed_time,3)
 print("\n")
 print("\n"+"Computation finished in :" + str(elapsed_time) + " seconds ")
 return elapsed_time 


main()