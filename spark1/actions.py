import numpy as np
import db

from importlib import reload

reload(db)

# controller id
c_id = 1


# action class. id= identifier of the action. source= node from which the data are moved/copied . destination=target node where data are moved/copied. Type= type of action. Description= description of the action. Delay= mean distance


class Node:
    def __init__(self, id, disk, availability, mean_delay):
        self.id = id
        self.disk = disk
        self.availability = availability
        self.mean_delay = mean_delay


class Action:

    def __init__(self, id, source, destination, type, description, delay, impacts, name_file, cost):
        self.id = id
        self.source = source
        self.destination = destination
        self.type = type
        self.description = description
        self.delay = delay
        self.impacts = impacts
        self.name_file = name_file
        self.cost = cost


def classmethod(CR_Action):
    pass


class CR_Action(Action):
    def __init__(self, id_data_set, id, source, destination, type, description, delay, impacts, name_file, cost):
        self.id_data_set = id_data_set
        self.id = id
        self.source = source
        self.destination = destination
        self.type = type
        self.description = description
        self.delay = delay
        self.impacts = impacts
        self.name_file = name_file
        self.cost = cost

    def set_data_set(cls, data_set_id):
        cls.id_data_set = data_set_id

    def update_vector(cls,string):
        cls.impacts = np.loadtxt(string, delimiter=",")

# list of available nodes in the net. fields: id, disk space,availability,mean delay from node 1

N1 = Node(1, 1, db.get_availability(1), db.get_latency(1, 1))
N2 = Node(2, 1, db.get_availability(2), db.get_latency(1, 2))
N3 = Node(3, 1, db.get_availability(3), db.get_latency(1, 3))

data_set_id = 1
# reference node
state = Node(0, 0, 0, 0)

node_list = [N1, N2, N3]

# costs, metadata associated to action type
cost_m = 1.5
cost_d = 1.8
cost_cr = 1

# list of actions for node 1
# Move actions
M12 = Action(0, N1, N2, "move", "move data from node 1 (locally) to node 2", N2.mean_delay,
             np.loadtxt("IM12.txt", delimiter=","), "IM12.txt", cost_m)
M21 = Action(1, N2, N1, "move", "move data from node 2 to node 1 (locally)", N1.mean_delay,
             np.loadtxt("IM21.txt", delimiter=","), "IM21.txt", cost_m)
M13 = Action(2, N1, N3, "move", "move data from node 1 (locally) to node 3", N3.mean_delay,
             np.loadtxt("IM13.txt", delimiter=","), "IM13.txt", cost_m)
M31 = Action(3, N3, N1, "move", "move data from node 3 to node 1 (locally)", N1.mean_delay,
             np.loadtxt("IM31.txt", delimiter=","), "IM31.txt", cost_m)
M32 = Action(4, N3, N2, "move", "move data from node 3 to node 2", N2.mean_delay, np.loadtxt("IM32.txt", delimiter=","),
             "IM32.txt", cost_m)
M23 = Action(5, N2, N3, "move", "move data from node 2 to node 3 ", N3.mean_delay,
             np.loadtxt("IM23.txt", delimiter=","), "IM23.txt", cost_m)

# Copy actions
C12 = Action(6, N1, N2, "copy", "copy data from node 1 (locally) to node 2", N2.mean_delay,
             np.loadtxt("IC12.txt", delimiter=","), "IC12.txt", cost_d)
C21 = Action(7, N2, N1, "copy", "copy data from node 2 to node 1 (locally) ", N1.mean_delay,
             np.loadtxt("IC21.txt", delimiter=","), "IC21.txt", cost_d)
C13 = Action(8, N1, N3, "copy", "copy data from node 1 (locally) to node 3", N3.mean_delay,
             np.loadtxt("IC13.txt", delimiter=","), "IC13.txt", cost_d)
C31 = Action(9, N3, N1, "copy", "copy data from node 3 to node 1 (locally)", N1.mean_delay,
             np.loadtxt("IC31.txt", delimiter=","), "IC31.txt", cost_d)
C32 = Action(10, N3, N2, "copy", "copy data from node 3 to node 2", N2.mean_delay,
             np.loadtxt("IC32.txt", delimiter=","), "IC32.txt", cost_d)
C23 = Action(11, N2, N3, "copy", "copy data from node 2 to node 3 ", N3.mean_delay,
             np.loadtxt("IC23.txt", delimiter=","), "IC23.txt", cost_d)

# Change reference copy actions

CR1 = CR_Action(0, 13, state, N1, "change reference copy", "change reference copy,to a copy hosted in node 1 (local copy)",
                N1.mean_delay,np.loadtxt("ICR1.txt", delimiter=","), "ICR1.txt", cost_cr)
CR2 = CR_Action(0, 14, state, N2, "change reference copy", "change reference copy,to a copy hosted in node 2",
                N2.mean_delay, np.loadtxt("ICR2.txt", delimiter=","), "ICR2.txt", cost_cr)

CR3 = CR_Action(0, 15, state, N3, "change reference copy", "change reference copy, to a copy hosted in node 3", N3.mean_delay, np.loadtxt("ICR3.txt", delimiter=","), "ICR3.txt", cost_cr)

# null action
NA = Action(12, 0, 0, "null", "Do Nothing", 0, [0, 0, 0, 0, 0], " ", 1)
# action list containing all possible actions
action_list = [M12, M21, M13, M31, M32, M23, C12, C21, C13, C31, C32, C23]


def update_impacts():
    global M12,M21,M13,M31,M32,M23,C12,C21,C13,C31,C32,C23

    M12.impacts = np.loadtxt("IM12.txt", delimiter=",")
    M21.impacts = np.loadtxt("IM21.txt", delimiter=",")
    M13.impacts = np.loadtxt("IM13.txt", delimiter=",")
    M31.impacts = np.loadtxt("IM31.txt", delimiter=",")
    M32.impacts = np.loadtxt("IM32.txt", delimiter=",")
    M23.impacts = np.loadtxt("IM23.txt", delimiter=",")
    C12.impacts = np.loadtxt("IC12.txt", delimiter=",")
    C21.impacts = np.loadtxt("IC21.txt", delimiter=",")
    C13.impacts = np.loadtxt("IC13.txt", delimiter=",")
    C31.impacts = np.loadtxt("IC31.txt", delimiter=",")
    C32.impacts = np.loadtxt("IC32.txt", delimiter=",")
    C23.impacts = np.loadtxt("IC23.txt", delimiter=",")
    CR1.impacts = np.loadtxt("ICR1.txt", delimiter=",")
    CR2.impacts = np.loadtxt("ICR2.txt", delimiter=",")
    CR3.impacts = np.loadtxt("ICR3.txt", delimiter=",")

# function used in order to update the attributes of a node
def update_state(node):
    global state
    state.id = node.id
    state.disk = node.disk
    state.availability = db.get_availability(node.id)
    state.mean_delay = db.get_latency(1, node.id)


def get_state():
    global state

    return state


def update_data_set(n):
    global data_set_id
    data_set_id = n


# map node id from db to node object
def set_state(n):
    for x in node_list:
        if x.id == n:
            update_state(x)
