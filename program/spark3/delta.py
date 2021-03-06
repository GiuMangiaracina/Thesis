import numpy as np
import metrics
import math

LEARNING_RATE = 0.5

v = [0, 0, 0, 0, 0, 0]


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


#  method which compares the metrics of two computations, and, calculating the Delta, updates the impact vector related to the action.
def delta(RT1, ET1, X1, NL1, A1, RT2, ET2, X2, NL2, A2, action):
    print("old impact vector: ")
    print("\n")
    print(action.impacts)

    # delta for response time
    dRT = RT2 - RT1
    a = -metrics.func(dRT, metrics.response_time.ro)

    v[0] = (1 - LEARNING_RATE) * action.impacts[0] + LEARNING_RATE * a
    v[0] = truncate(v[0], 2)
    # delta for ex time
    dET = ET2 - ET1
    b = -metrics.func(dET, metrics.execution_time.ro)

    v[1] = (1 - LEARNING_RATE) * action.impacts[1] + LEARNING_RATE * b
    v[1] = truncate(v[1], 2)
    # delta for throughput
    dX = X2 - X1
    c = metrics.func(dX, metrics.throughput.ro)

    v[2] = (1 - LEARNING_RATE) * action.impacts[2] + LEARNING_RATE * c
    v[2] = truncate(v[2], 2)
    # delta for latency
    dl = NL2 - NL1
    d = -metrics.func(dl, metrics.latency.ro)

    v[3] = (1 - LEARNING_RATE) * action.impacts[3] + LEARNING_RATE * d
    v[3] = truncate(v[3], 2)
    # delta for availability
    dA = A2 - A1
    k = metrics.func(dA, metrics.availability.ro)

    v[4] = (1 - LEARNING_RATE) * action.impacts[4] + LEARNING_RATE * k
    v[4] = truncate(v[4], 2)

    # delta for data consistency
    if action.type == "copy":
        dc = - 1 / metrics.k
    else:
        dc = 0
    g = metrics.func(dc, metrics.d_c.ro)

    v[5] = (1 - LEARNING_RATE) * action.impacts[5] + LEARNING_RATE * g

    print("new impact vector :")
    print("\n")
    print(v)

    np.savetxt(action.name_file, v, delimiter=',')
