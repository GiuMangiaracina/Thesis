import numpy as np
import math

# variables for data consistency: k = max number of copies;
k = 2
dc = 1

# weights associated to score function
w1 = 0.7
w2 = 0.3


# metric class:
# min = minimum threshold value; max = maximum threshold value ;
# type = 0 if Qos positive metric, 1 if QoS negative metric;
# ro = selected rho parameter.
class Metric:

    def __init__(self, min, max, type, ro):
        self.min = min
        self.max = max
        self.type = type
        self.ro = ro


# instantiate the metrics-> requirements. NB: in init.check function are checked only the metrics belonging to the requirements of the application.
response_time = Metric(0, 30, 1, 40)
latency = Metric(0, 1600, 1, 2000)
execution_time = Metric(0, 30, 1, 15)

# data consistency
d_c = Metric(0.4, 1, 0, 1 / k)

throughput = Metric(30000, 0, 0, 3000)
availability = Metric(80, 0, 0, 25)


# function used to truncate floats
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


# function used to define numerically the impact of an action on a particular metric. delta= M(t+1) - M (t)
def func(delta, ro):
    x = math.pi / 2
    out = np.arctan(delta * x * 1 / ro)
    if out >= 1:
        out = 1
    if out <= -1:
        out = -1
    if out > - 1 and out < 1:
        out = truncate(out, 3)

    return out


def update_dc(n):
    global dc
    dc = 1 - n * (1 / k)
