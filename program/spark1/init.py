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

from termcolor import colored
import shlex
import sys

n_init = 0

block = 0
# initial weights
w_1 = 1
w_2 = 1

# variables indicating the status of metrics: 1 = satisfied, 0 = not satisfied

response_time_status = 1
latency_status = 1
execution_time_status = 1
throughput_status = 1
availability_status = 1
dc_status = 1

# penalty factor (b)

penalty_factor = 0.33


# this method initializes the application. It adds the proxy, adds the toxicity of type latency to it, and finally it starts the history server
def init():
    print("Initializing")

    # add proxy

    with open('add.json', 'r') as jsonfile:
        json_content = json.load(jsonfile)
    json_content["name"] = "minioProxy" + str(actions.c_id)
    json_content["listen"] = "127.0.0.1:800" + str(actions.c_id)

    with open('add.json', 'w') as jsonfile:
        json.dump(json_content, jsonfile, indent=4)
    subprocess.call(["./addProxy.sh"], shell=True)

    # set initial latency
    # l = int(input ("\n"+"set toxic, latency: "+"\n"))
    subprocess.call(shlex.split('./set.sh minioProxy' + str(actions.c_id)))
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
    subprocess.call(["./modify.sh"], shell=True)


# method used to truncate floats (to max digits number )
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


# this method checks the status of each metric compared to the user requirements. n = the node in which the data resides.
def check(RT, ET, X, NL, n):
    available_actions = [actions.NA]
    global n_init
    list = []
    rand = 0

    global latency_status, execution_time_status, throughput_status, availability_status, response_time_status, dc_status, w_1, w_2, block
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

    availability = actions.state.availability

    if availability < metrics.availability.min:
        availability_status = 0
    else:

        availability_status = 1

    if metrics.dc < metrics.d_c.min:
        dc_status = 0
    else:
        dc_status = 1

    # print the user goal. only the metrics belonging to the user goal are printed.
    print("\n")
    print("Goal: RT < " + str(metrics.response_time.max) + " s AND A >= " + str(metrics.availability.min) + "%")
    print("\n")
    print("Metric status: " + "\n")
    print("response time : " + str(response_time_status))
    # print ("latency : " + str(latency_status))
    # print("execution time : " + str(execution_time_status))
    # print("throughput : " + str(throughput_status))
    print("availability : " + str(availability_status))
    # print("data consistency : " + str(dc_status))
    print("\n")

    # Goal check
    if not (response_time_status and availability_status):

        # leave negative feedback
        tsViol = int(time.time())
        abort = db.set_data(actions.data_set_id)
        if abort != n_init:
            return 0

        db.feedback(tsViol)

        # start action selection process: create available action list
        actions.update_impacts()
        for a in actions.action_list:

            if a.source.id == n.id and a.destination.disk == 1:
                available_actions.append(a)

            else:
                pass

        # add available change reference actions to the action list
        list = instantiate_cr_actions()
        available_actions.extend(list)
        random.shuffle(available_actions)

        # print ("Goal violated. Repair Action needed. Available actions: " + "\n")
        print(colored('Goal violated. Repair Action needed. Available actions: ' + '\n', 'red'))
        # draw a random number between 0 and 1
        z = random.uniform(0, 1)

        # explore
        if z > 0.9:
            selected = random.choice(available_actions)
            print(colored('Random action selected', 'yellow'))
            # print ("Random action selected")
            rand = 1
        # exploit
        else:

            max = -2
            for b in available_actions:

                # retrieve from the impacts associated to the actions
                # the effects on the response_time and availability
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

                # handle the cases
                if (response_time_status == 0 and availability_status == 1):

                    # compute score (internal impact)
                    score = (w_1 * r_s + w_2 * neg_av) / b.cost
                    score = truncate(score, 2)

                    # read counter from db (external impact)
                    c = db.read_counter(b)
                    # compute global score
                    score_p = score * (1 - penalty_factor * c)

                elif (response_time_status == 1 and availability_status == 0):

                    # compute score (internal impact)
                    score = (w_2 * neg_rs + w_1 * a_s) / b.cost
                    score = truncate(score, 2)
                    # read counter from db (external impact)
                    c = db.read_counter(b)
                    # compute global score
                    score_p = score * (1 - penalty_factor * c)

                elif (response_time_status == 0 and availability_status == 0):
                    # compute score (internal impact)
                    score = ((r_s + a_s) / 2) / b.cost
                    score = truncate(score, 2)
                    # read counter from db (external impact)
                    c = db.read_counter(b)
                    # compute global score
                    score_p = score * (1 - penalty_factor * c)

                print(str(b.description) + ". Internal score: " + str(score) + "; Global score_p:" + str(score_p))

                if score_p > max:
                    max = score_p
                    selected = b

                w_1 = 1
                w_2 = 1

        # print("\n" + "Selected action: " + str(selected.description))
        print(colored('\n' + 'Selected action: ' + str(selected.description), 'yellow'))
        # insert selected action into event table
        event_id = db.insert_action(selected, rand)

        print(str(event_id))
        # call the method which will close the feedback process after T (except for null actions)
        if selected.id != 0:
            db.close_T(event_id)

        if selected.type == "move":
            # update position of data set
            db.update_data(actions.data_set_id, selected.destination.id)
            # lock the shared block variable for 10 seconds ("execution time" of the action )
      #      db.lock_computation()
       #     time.sleep(10)
        #    db.unlock_computation()

        elif selected.type == "copy":
            # add new data set row
            data_set_id = db.add_data(selected.destination.id)
            # update application reference data set id
            actions.update_data_set(data_set_id)

        elif selected.type == "change reference copy":
            # update application reference data set id
            actions.update_data_set(selected.id_data_set)

        # retrieve data set position
        pos = db.set_data(actions.data_set_id)

        # start new computation
        if selected.id != 0:
            availability_old_state = actions.get_state().availability
            # update state
            actions.set_state(pos)

            RT2, ET2, X2, NL2 = computation_2(actions.state)

            # calculate the delta
            delta.delta(RT, ET, X, NL, availability_old_state, RT2, ET2, X2, NL2, actions.state.availability, selected)

            p = check(RT2, ET2, X2, NL2, actions.state)

    else:

        print(colored("Goal not violated.", 'green'))

    return 1


# Method used to start a computation. n =the node in which the data resides
def computation(n):
    # m = latency, calculated with a normal distribution of mean retrieved from the reference node
    m = int(round(np.random.normal(n.mean_delay, 7)))
    if m <= 0:
        m = 0
    # change latency of the proxy
    modify(m)
    print("\n")
    # launch the spark application
    subprocess.call(["./app.sh"], shell=True)

    time.sleep(1)

    # retrieve the metrics of the completed computation from the monitoring program
    RT, ET, X, NL = monitoring.main()
    # check the number of the copies existing in the environment
    copies_number = db.check_dc()
    # update dc metric
    metrics.update_dc(copies_number)
    print("data consistency: " + str(metrics.dc))
    print("availability: " + str(actions.state.availability) + " %")

    # check the status of the metrics

    r = check(RT, ET, X, NL, n)

    if r == 0:
        # case in which there is a conflicting action selection process
        print("restart computation with updated position of data set.")

        return 0

    return 1


def computation_2(n):
    global n_init
    n_init = n.id

    m = int(round(np.random.normal(n.mean_delay, 7)))
    if m <= 0:
        m = 0
    modify(m)
    print("\n")
    subprocess.call(["./app.sh"], shell=True)
    time.sleep(1)

    # retrieve the metrics of the completed computation from the monitoring program
    RT, ET, X, NL = monitoring.main()

    copies_number = db.check_dc()
    metrics.update_dc(copies_number)

    print("data consistency: " + str(metrics.dc))
    print("availability: " + str(actions.state.availability) + " %")

    yield RT
    yield ET
    yield X
    yield NL


def __main__():
    # check if the application has been initialized -> needed only for the first time
    with open('goal.json', 'r') as jsonfile:
        json_content = json.load(jsonfile)
    if json_content['initialized'] == 0:
        init()
    else:
        # generate action list
        c = actions.generate_actions(actions.node_list)
        if c == 0:
            print(
                colored(
                    "CAUTION: SOME OF THE VECTORS OF IMPACTS ARE MISSING. PLEASE LAUNCH THE TRAINING PROGRAM ('training.py').",
                    'red'))
            sys.exit()

        # fill initial gpw table
        if db.check_gpw_table() == 0:
            db.fill_in_gpw()

        # infinite loop which starts the computations
        while 1:
            # time.sleep(random.randint(20,60))
            # int(round(np.random.normal(20, 7)))
            # arrival rate
            x = int(round(np.random.normal(15, 2)))
            if x < 0:
                x = 0
            time.sleep(x)
            # print ("Start APP 1;")
            print(colored("Start APP " + str(actions.c_id), 'green'))
            setting()


# method used to lookup the file_table in order to set the position of data and map to node
def setting():
    global n_init
    n_init = db.set_data(actions.data_set_id)

    actions.set_state(n_init)

    print("reference copy id: " + str(actions.data_set_id))
    code = computation(actions.state)

    print(str(code))
    if code == 0:
        print("computation returned with code 0 ")


# method used to instantiate at run-time the available CR actions
def instantiate_cr_actions():
    list = []
    CR_actions = actions.cr_action_list
    records = db.lookup_data()
    source_node = actions.state.id
    for row in records:
        if row[0] != actions.data_set_id and row[1] != actions.state.id:
            for a in CR_actions:
                if row[1] == a.destination.id:
                    a.set_data_set(row[0])
                    # derive impacts from associated movement actions
                    string = 'IM' + str(source_node) + str(a.destination.id) + '.txt'
                    a.update_vector(string)
                    list.append(a)
    return list


if __name__ == "__main__":
    __main__()
