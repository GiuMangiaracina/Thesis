import monitoring
import metrics
import json
import os
import subprocess
import time
import actions
import numpy as np
from termcolor import colored

action_list = []


def generate_actions():
    global action_list
    node_list = actions.node_list
    id = 1
    v = [0, 0, 0, 0, 0, 0]
    for n in node_list:

        for c in node_list:
            if (c.id != n.id):

                # create missing text files

                if not os.path.exists("output_training/IM" + str(n.id) +"_"+ str(c.id) + ".txt"):
                    os.mknod("output_training/IM" + str(n.id) +"_"+ str(c.id) + ".txt")
                    np.savetxt("output_training/IM" + str(n.id) +"_"+ str(c.id) + ".txt", v, delimiter=',')

                    os.mknod("output_training/IC" + str(n.id) + "_"+str(c.id) + ".txt")
                    np.savetxt("output_training/IC" + str(n.id) + "_"+str(c.id) + ".txt", v, delimiter=',')

                    # generate movement actions
                    a = actions.Action(id, n, c, 'move', 'move data from ' + str(n.id) + ' to ' + str(c.id), c.mean_delay,
                                   np.loadtxt("output_training/IM" + str(n.id) +"_"+ str(c.id) + ".txt", delimiter=","),
                                   "output_training/IM" + str(n.id) +"_"+ str(c.id) + ".txt", actions.cost_m,
                                   "IM" + str(n.id) + str(c.id))
                    action_list.append(a)

                if not os.path.exists("output_training/ICR" + str(n.id) + ".txt"):
                    os.mknod("output_training/ICR" + str(n.id) + ".txt")
                    np.savetxt("output_training/ICR" + str(n.id) + ".txt", v, delimiter=',')


                id = id + 1


# function used to modify the latency to toxiproxy
def modify(n):
    with open('template.json', 'r') as jsonfile:
        json_content = json.load(jsonfile)
        json_content["attributes"]["latency"] = n
        subprocess.call(["./modify.sh"])

    with open('template.json', 'w') as jsonfile:
        json.dump(json_content, jsonfile, indent=4)
    subprocess.call(["./modify.sh"])


# the function starts the computation and outputs the metrics from the monitoring system.
def computation(n):
    FNULL = open(os.devnull, "w")
    modify(n)
    subprocess.call(["./app.sh"], stdout=FNULL, stderr=subprocess.STDOUT)
    time.sleep(1)

    # retrieve the metrics of the completed computation from the monitoring program
    RT, ET, X, NL = monitoring.main()

    yield RT
    yield ET
    yield X
    yield NL


def training():
    # N = number of iterations of the process
    N = 5
    generate_actions()

    z = 0
    q = 0
    p = 0
    r = 0

    print("TRAINING STARTED.\n")
    for a in action_list:
        vector = []
        print(a.label + " :\n")
        for i in range(0, N, 1):
            print("iteration number " + str(i + 1) + ":\n")

            RT1, ET1, X1, NL1 = computation(a.source.mean_delay)
            print("first computation finished (source)")
            RT2, ET2, X2, NL2 = computation(a.destination.mean_delay)
            print("second computation finished (destination)")

            dRT = RT2 - RT1
            s = -metrics.func(dRT, metrics.response_time.ro)
            z = z + s

            dET = ET2 - ET1
            b = -metrics.func(dET, metrics.execution_time.ro)
            q = q + b

            dX = X2 - X1
            c = metrics.func(dX, metrics.throughput.ro)
            p = p + c

            dl = NL2 - NL1
            d = -metrics.func(dl, metrics.latency.ro)
            r = r + d

        vector.append(z / N)
        vector.append(q / N)
        vector.append(p / N)
        vector.append(r / N)

        k = metrics.func(a.destination.availability - a.source.availability, metrics.availability.ro)
        vector.append(k)
        print("impact vector for movement action " + a.label + " :\n")
        for v in vector:
            print(v)

        z = 0
        q = 0
        p = 0
        r = 0

        # save impact vector for movement action
        with open(a.name_file, "w") as f:
            for x in vector:
                f.write(str(x) + "\n")

        # save impact vector for copy action
        with open("output_training/IC" + str(a.source.id) + "_"+str(a.destination.id) + ".txt", "w") as f:
            for x in vector:
                f.write(str(x) + "\n")
    print(colored("TRAINING COMPLETED.", 'green'))


training()
