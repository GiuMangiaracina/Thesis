import monitoring
import metrics
import json
import os
import subprocess
import time
import actions


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
    # N = number of times each action is taken
    N = 5
    IM12 = []
    IM13 = []
    IM21 = []

    IM31 = []
    IM23 = []
    IM32 = []

    z = 0
    q = 0
    p = 0
    r = 0

    # each action is taken N times. The delta of each action is calculated, and the mean value is stored in the vector of impact of the relative action
    i = 0
    # action M12
    for i in range(0, N, 1):
        RT1, ET1, X1, NL1 = computation(actions.N1.mean_delay)
        print("finished first")
        RT2, ET2, X2, NL2 = computation(actions.N2.mean_delay)
        print("finished second")

        dRT = RT2 - RT1
        a = -metrics.func(dRT, metrics.response_time.ro)
        z = z + a
        print(str(z))

        dET = ET2 - ET1
        b = -metrics.func(dET, metrics.execution_time.ro)
        q = q + b

        dX = X2 - X1
        c = metrics.func(dX, metrics.throughput.ro)
        p = p + c

        dl = NL2 - NL1
        d = -metrics.func(dl, metrics.latency.ro)
        r = r + d

    IM12.append(z / N)
    IM12.append(q / N)
    IM12.append(p / N)
    IM12.append(r / N)

    k = metrics.func(actions.N2.availability - actions.N1.availability, metrics.availability.ro)
    IM12.append(k)
    print("vector impact for M12 " + str(IM12))

    z = 0
    q = 0
    p = 0
    r = 0
    i = 0
    # Action M13
    for i in range(0, N, 1):
        RT1, ET1, X1, NL1 = computation(actions.N1.mean_delay)
        print("finished first")
        RT2, ET2, X2, NL2 = computation(actions.N3.mean_delay)
        print("finished second")

        dRT = RT2 - RT1
        e = -metrics.func(dRT, metrics.response_time.ro)
        z = z + e

        dET = ET2 - ET1
        f = -metrics.func(dET, metrics.execution_time.ro)
        q = q + f

        dX = X2 - X1
        g = metrics.func(dX, metrics.throughput.ro)
        p = p + g

        dl = NL2 - NL1
        h = -metrics.func(dl, metrics.latency.ro)
        r = h + r

    IM13.append(z / N)
    IM13.append(q / N)
    IM13.append(p / N)
    IM13.append(r / N)
    i = metrics.func(actions.N3.availability - actions.N1.availability, metrics.availability.ro)
    IM13.append(i)
    print("vector impact for M13 " + str(IM13))

    z = 0
    q = 0
    p = 0
    r = 0
    ep = 0
    # Action M21
    for ep in range(0, N, 1):
        RT1, ET1, X1, NL1 = computation(actions.N2.mean_delay)
        print("finished first")
        RT2, ET2, X2, NL2 = computation(actions.N1.mean_delay)
        print("finished second")

        dRT = RT2 - RT1
        e = -metrics.func(dRT, metrics.response_time.ro)
        z = z + e

        dET = ET2 - ET1
        f = -metrics.func(dET, metrics.execution_time.ro)
        q = q + f

        dX = X2 - X1
        g = metrics.func(dX, metrics.throughput.ro)
        p = p + g

        dl = NL2 - NL1
        h = -metrics.func(dl, metrics.latency.ro)
        r = h + r

    ep = 0
    IM21.append(z / N)
    IM21.append(q / N)
    IM21.append(p / N)
    IM21.append(r / N)

    m = metrics.func(actions.N1.availability - actions.N2.availability, metrics.availability.ro)
    IM21.append(m)
    print("vector impact for IM21 " + str(IM21))


    z = 0
    q = 0
    p = 0
    r = 0

    # action M31
    for ep in range(0, N, 1):
        RT1, ET1, X1, NL1 = computation(actions.N3.mean_delay)
        print("finished first")
        RT2, ET2, X2, NL2 = computation(actions.N1.mean_delay)
        print("finished second")

        dRT = RT2 - RT1
        a = -metrics.func(dRT, metrics.response_time.ro)
        z = z + a
        print(str(z))

        dET = ET2 - ET1
        b = -metrics.func(dET, metrics.execution_time.ro)
        q = q + b

        dX = X2 - X1
        c = metrics.func(dX, metrics.throughput.ro)
        p = p + c

        dl = NL2 - NL1
        d = -metrics.func(dl, metrics.latency.ro)
        r = r + d

    IM31.append(z / N)
    IM31.append(q / N)
    IM31.append(p / N)
    IM31.append(r / N)

    k = metrics.func(actions.N1.availability - actions.N3.availability, metrics.availability.ro)
    IM31.append(k)
    print("vector impact for M31 " + str(IM31))

    z = 0
    q = 0
    p = 0
    r = 0
    ep = 0
    # Action M23
    for ep in range(0, N, 1):
        RT1, ET1, X1, NL1 = computation(actions.N2.mean_delay)
        print("finished first")
        RT2, ET2, X2, NL2 = computation(actions.N3.mean_delay)
        print("finished second")

        dRT = RT2 - RT1
        e = -metrics.func(dRT, metrics.response_time.ro)
        z = z + e

        dET = ET2 - ET1
        f = -metrics.func(dET, metrics.execution_time.ro)
        q = q + f

        dX = X2 - X1
        g = metrics.func(dX, metrics.throughput.ro)
        p = p + g

        dl = NL2 - NL1
        h = -metrics.func(dl, metrics.latency.ro)
        r = h + r

    IM23.append(z / N)
    IM23.append(q / N)
    IM23.append(p / N)
    IM23.append(r / N)
    i = metrics.func(actions.N3.availability - actions.N2.availability, metrics.availability.ro)
    IM23.append(i)
    print("vector impact for M23 " + str(IM23))

    z = 0
    q = 0
    p = 0
    r = 0
    ep = 0
    # Action M32
    for ep in range(0, N, 1):
        RT1, ET1, X1, NL1 = computation(actions.N3.mean_delay)
        print("finished first")
        RT2, ET2, X2, NL2 = computation(actions.N2.mean_delay)
        print("finished second")

        dRT = RT2 - RT1
        e = -metrics.func(dRT, metrics.response_time.ro)
        z = z + e

        dET = ET2 - ET1
        f = -metrics.func(dET, metrics.execution_time.ro)
        q = q + f

        dX = X2 - X1
        g = metrics.func(dX, metrics.throughput.ro)
        p = p + g

        dl = NL2 - NL1
        h = -metrics.func(dl, metrics.latency.ro)
        r = h + r

    IM32.append(z / N)
    IM32.append(q / N)
    IM32.append(p / N)
    IM32.append(r / N)

    m = metrics.func(actions.N2.availability - actions.N3.availability, metrics.availability.ro)
    IM32.append(m)
    print("vector impact for IM32 " + str(IM32))

    # save results to file texts
    with open("M12.txt", "w") as f:
        for s in IM12:
            f.write(str(s) + "\n")

    with open("M13.txt", "w") as f:
        for s in IM13:
            f.write(str(s) + "\n")

    with open("M21.txt", "w") as f:
        for s in IM21:
            f.write(str(s) + "\n")

    with open("M31.txt", "w") as f:
        for s in IM31:
            f.write(str(s) + "\n")

    with open("M23.txt", "w") as f:
        for s in IM23:
            f.write(str(s) + "\n")

    with open("M32.txt", "w") as f:
        for s in IM32:
            f.write(str(s) + "\n")


training()
