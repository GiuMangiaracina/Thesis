import numpy as np
import db
import os

from importlib import reload
reload(db)

#controller id
c_id=3

#action lists
total_action_list = []
action_list = []
cr_action_list = []


#action class. id= identifier of the action. source= node from which the data are moved/copied .
#destination=target node where data are moved/copied. Type= type of action.
# Description= description of the action. Delay = mean distance; impacts = vector of impacts;
#name_file = name of the vector file; cost=cost of the action.
class Action:

    def __init__(self,id,source,destination,type, description, delay,impacts,name_file,cost,label):
        self.id = id
        self.source = source
        self.destination = destination
        self.type = type
        self.description = description
        self.delay = delay
        self.impacts=impacts
        self.name_file= name_file
        self.cost = cost
        self.label=label

    def update_impacts(cls):
        cls.impacts = np.loadtxt(cls.name_file, delimiter=",")
def classmethod(CR_Action):
    pass

#Change Reference copy class action. id_data_set = id of the associated data set
class CR_Action(Action):
    def __init__(self,id_data_set, id,source,destination,type, description, delay,impacts,name_file,cost,label):
        self.id_data_set=id_data_set
        self.id = id
        self.source = source
        self.destination = destination
        self.type = type
        self.description = description
        self.delay = delay
        self.impacts=impacts
        self.name_file= name_file
        self.cost = cost
        self.label=label

    def set_data_set(cls,data_set_id):
        cls.id_data_set = data_set_id



    def update_vector(cls,string):
        cls.impacts = np.loadtxt(string, delimiter=",")

    def update_impacts(cls):
        cls.impacts = np.loadtxt(cls.name_file, delimiter=",")

#Node class. id = identifier of the node; disk = availability of the node to host the data set
#-> it is used to block actions; availability= mean availability of the node;
#mean delay = mean latency from the node in which the app is placed (3), and the specific node
class Node:
    def __init__(self,id,disk,availability,mean_delay):
        self.id = id
        self.disk = disk
        self.availability = availability
        self.mean_delay = mean_delay



#list of available nodes in the net.
N1 = Node(1,1,db.get_availability(1), db.get_latency(3,1))
N2 = Node(2,1,db.get_availability(2), db.get_latency(3,2))
N3 = Node(3,1,db.get_availability(3), db.get_latency(3,3))

node_list = [N1,N2,N3]
#id of the reference copy of the application
data_set_id = 1
#reference node
state = Node(0,0,0,0)

# costs, metadata associated to action type (1)+ monetary cost ($/GB)
cost_m = 1.5
cost_d = 1.8
cost_cr = 1

# null action

NA = Action(0, 0, 0, "null", "Do Nothing", 0, [0, 0, 0, 0, 0], " ", 1,"NA")



#method used to update the value of the impacts at run-time
def update_impacts():
    global action_list
    for a in action_list:
        a.update_impacts()

#function used in order to update the attributes of a node
def update_state(node):
    global state
    state.id=node.id
    state.disk=node.id
    state.availability = db.get_availability(node.id)
    state.mean_delay = db.get_latency(3, node.id)

#method used to update the actual data set id
def update_data_set(n):
    global data_set_id
    data_set_id=n

#method which retuns the actual state
def get_state():
    return state

#map node id from db to node object
def set_state(n):

    for x in node_list:
        if x.id == n:
            update_state(x)



def generate_actions(node_list):
    global total_action_list, cr_action_list, action_list
    id=1


    for n in node_list:

        for c in node_list:
            if (c.id!= n.id):

                if not os.path.exists("IM" + str(n.id) + str(c.id) + ".txt"):
                    return 0




                a = Action(id,n,c,'move','move data from '+str(n.id)+' to '+ str(c.id),c.mean_delay,np.loadtxt("IM"+str(n.id)+str(c.id)+".txt", delimiter=","),"IM"+str(n.id)+str(c.id)+".txt",cost_m,"IM"+str(n.id)+str(c.id))
                action_list.append(a)
                id = id+1
                b =  Action(id,n,c,'copy','copy data from '+str(n.id)+' to '+ str(c.id),c.mean_delay,np.loadtxt("IC"+str(n.id)+str(c.id)+".txt", delimiter=","),"IC"+str(n.id)+str(c.id)+".txt",cost_d,"IC"+str(n.id)+str(c.id))
                action_list.append(b)
                id = id+1


    for c in node_list:
        cr = CR_Action(0,id,state,c,"change reference copy","change reference copy, to a copy hosted in node "+str(c.id),c.mean_delay, np.loadtxt("ICR"+str(c.id)+".txt", delimiter=","),"ICR"+str(c.id)+".txt", cost_cr,"ICR"+str(c.id))
        id = id+1
        cr_action_list.append(cr)

    total_action_list = action_list + cr_action_list
    total_action_list.append(NA)
