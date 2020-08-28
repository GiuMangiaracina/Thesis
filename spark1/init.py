import subprocess
import os
import time
import json
import math
import numpy as np
import random
import monitoring
import metrics
import actions
import delta
import db

block=0
# weights
w_1 = 1
w_2 = 1

# global status metrics
response_time_status = 1
latency_status = 1
execution_time_status = 1

throughput_status = 1
availability_status = 1

dc_status = 1

# penalty factor (b)

penalty_factor = 0.33


# this method initializes the application. It adds the proxy, add the toxicity of type latency to it, and finally it starts the history server
def init():
    print("Initializing")

    # add proxy
    subprocess.call(["./addProxy.sh"])
    print("\n" + "\n" + "Proxy added")
    # set initial latency
    # l = int(input ("\n"+"set toxic, latency: "+"\n"))
    subprocess.call(["./set.sh"])

    # start the history server
    os.system("../sbin/start-history-server.sh ")

    with open('goal.json', 'r') as jsonfile:
        json_content = json.load(jsonfile)

    json_content["initialized"] = 1

    with open('goal.json', 'w') as jsonfile:
        json.dump(json_content, jsonfile, indent=4)


# method used to modify the latency to the proxy
def modify(n):
    with open('template.json', 'r') as jsonfile:
        json_content = json.load(jsonfile)
        json_content["attributes"]["latency"] = n

    with open('template.json', 'w') as jsonfile:
        json.dump(json_content, jsonfile, indent=4)
    subprocess.call(["./modify.sh"])

    # method used to truncate floats


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


# update status of each metric. n = the node in which the data resides.
def check(RT, ET, X, NL, n):
    available_actions = [actions.NA]
    list = []
    rand=0

    global latency_status, execution_time_status, throughput_status, availability_status, response_time_status, dc_status, w_1, w_2,block
    if RT > metrics.response_time.max:
        response_time_status = 0
    else:
        response_time_status = 1

    if ET > metrics.execution_time.max:
        execution_time_status = 0
    else:
        execution_time_status = 1

    if X < metrics.throughput.min:
        throughput_status = 0


    else:
        throughput_status = 1

    if NL > metrics.latency.max:
        latency_status = 0
    else:
        latency_status = 1

    # associates availability to node
    # for x in actions.node_list:
    #   if x.id == n:
    availability = actions.state.availability

    if availability < metrics.availability.min:
        availability_status = 0
    else:

        availability_status = 1

    if metrics.dc < metrics.d_c.min:
        dc_status = 0
    else:
        dc_status = 1
    print("\n")
    print ("Goal: RT < "+str(metrics.response_time.max)+" s AND A >= "+str(metrics.availability.min)+"%")
    print("\n")
    print ("Metric status: " + "\n")
    print("response time : " + str(response_time_status))
    #print ("latency : " + str(latency_status))
   # print("execution time : " + str(execution_time_status))
    #print("throughput : " + str(throughput_status))
    print("availability : " + str(availability_status))
    #print("data consistency : " + str(dc_status))
    print ("\n")

    # Goal check
    if not (response_time_status and availability_status):



        # leave negative feedback
        tsViol = int(time.time())

        while db.check_computation():
            print ("another controller is moving the data_set: wait execution time.")
            block=1

        if block==1:
           block=0
           return 0

        block=0
        db.feedback(tsViol)
        # start action selection process
        actions.update_impacts()
        for a in actions.action_list:
            if a.source.id == n.id and a.destination.disk == 1 :
                available_actions.append(a)

            else:
                pass

        # add available change reference actions to the action list
        list = instantiate_cr_actions()
        available_actions.extend(list)
        random.shuffle(available_actions)




        print ("Goal violated. Repair Action needed. Available actions: " + "\n")

        #
        z = random.uniform(0, 1)

        if z > 0.9:
            selected = random.choice(available_actions)
            print ("Random action selected")
            rand=1
        else:

            max = -2
            for b in available_actions:

                # response_time and availability
                neg_rs = 0
                neg_av = 0
                r_s = b.impacts[0]
                if r_s < 0:
                    neg_rs = r_s
                    w_1 = metrics.w1
                    w_2 = metrics.w2

                a_s = b.impacts[4]
                if a_s < 0:
                    neg_av = a_s
                    w_1 = metrics.w1
                    w_2 = metrics.w2

                if (response_time_status == 0 and availability_status == 1):

                    score = (w_1 * r_s + w_2 * neg_av) / b.cost
                    score = truncate(score, 2)

                    # compute score_p

                    c = db.read_counter(b)

                    score_p = score * (1 - penalty_factor * c)



                elif (response_time_status == 1 and availability_status == 0):

                    score = (w_2 * neg_rs + w_1 * a_s)/b.cost
                    score = truncate(score , 2)

                    c = db.read_counter(b)
                    score_p = score * (1 - penalty_factor * c)
                elif (response_time_status == 0 and availability_status == 0):

                    score = ((r_s + a_s) / 2)/b.cost
                    score = truncate(score , 2)

                    c = db.read_counter(b)
                    score_p = score * (1 - penalty_factor * c)

                print (str(b.description) + ". Internal score: " + str(score) + "; Global score_p:" + str(score_p))

                if score_p > max:
                    max = score_p
                    selected = b

                w_1=1
                w_2=1

        print("\n" + "Selected action: " + str(selected.description))
        event_id = db.insert_action(selected,rand)

        print(str(event_id))
        if selected.id != 12:
            db.close_T(event_id)

        # update position of data set
        if selected.type == "move":
            db.update_data(actions.data_set_id, selected.destination.id)

            db.lock_computation()
            time.sleep(10)
            db.unlock_computation()

        elif selected.type == "copy":
            data_set_id = db.add_data(selected.destination.id)
            actions.update_data_set(data_set_id)

        elif selected.type == "change reference copy":
            actions.update_data_set(selected.id_data_set)

        n = db.set_data(actions.data_set_id)

        # start new computation
        if selected.id != 12:


            availability_old_state = actions.get_state().availability

            actions.set_state(n)


            RT2, ET2, X2, NL2 = computation_2(actions.state)

            delta.delta(RT, ET, X, NL, availability_old_state, RT2, ET2, X2, NL2, actions.state.availability, selected)
            
            p=check(RT2, ET2, X2, NL2, actions.state)





    else:
        print ("Goal not violated.")

    return 1


# Method used to start a computation. n = the id of the node in which the data resides
def computation(n):
    # for x in actions.node_list:
    #   if x.id == n:
    #      m=x.mean_delay

    m = int(round(np.random.normal(n.mean_delay, 7)))
    if m <= 0:
        m = 0

    modify(m)
    print("\n")
    subprocess.call(["./app.sh"])
    time.sleep(1)

    # retrieve the metrics of the completed computation from the monitoring program
    RT, ET, X, NL = monitoring.main()

    copies_number = db.check_dc()
    metrics.update_dc(copies_number)
    print ("data consistency: " + str(metrics.dc))
    print ("availability: " + str(actions.state.availability) + " %")

    # check the status of the metrics


    r=check(RT, ET, X, NL, n)

    if r==0:
        print ("restart computation with updated position of data set.")
        r=3


        return 0


    return 1

def computation_2(n):
    m = int(round(np.random.normal(n.mean_delay, 7)))
    if m <= 0:
        m = 0
    modify(m)
    print("\n")
    subprocess.call(["./app.sh"])
    time.sleep(1)

    # retrieve the metrics of the completed computation from the monitoring program
    RT, ET, X, NL = monitoring.main()

    copies_number = db.check_dc()
    metrics.update_dc(copies_number)
    print ("data consistency: " + str(metrics.dc))
    print ("availability: " + str(actions.state.availability) + " %")

    yield RT
    yield ET
    yield X
    yield NL


def __main__():

    with open('goal.json', 'r') as jsonfile:
        json_content = json.load(jsonfile)
    if json_content['initialized'] == 0:
        init()
    else:
         while 1:
                #time.sleep(random.randint(20,60))
                #int(round(np.random.normal(20, 7)))
                x =int(round(np.random.normal(15, 2)))
                if x<0:
                   x=0
                time.sleep(x)
                print ("Start APP 1;")
                setting()





        # db.unlock_computation()


# method used to lookup the file_table in order to set the position of data and map to node
def setting():
    n = db.set_data(actions.data_set_id)

    actions.set_state(n)

    print("reference copy id: "+ str(actions.data_set_id))
    code=computation(actions.state)

    print (str(code))
    if code==0:
        print("computation returned with code 0 ")
   




def instantiate_cr_actions():
    list = []
    CR_actions = [actions.CR1, actions.CR2, actions.CR3]
    records = db.lookup_data()
    source_node = actions.state.id
    for row in records:
        if row[0] != actions.data_set_id and row[1] != actions.state.id:
            for a in CR_actions:
                if row[1] == a.destination.id:
                    a.set_data_set(row[0])
                    string = 'IM'+ str(source_node)+str(a.destination.id)+'.txt'
                    a.update_vector(string)
                    list.append(a)
    return list


if __name__ == "__main__":
    __main__()
