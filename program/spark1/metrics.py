import numpy as np
import math

# variables for data consistency: k = max number of copies;
k = 2
dc = 1

# weights associated to score function
w1 = 0.7
w2 = 0.3


# metric class: min = minimum value; max = maximum value ;
# type = 0 if Qos positive metric, 1 if QoS negative metric;
# status : 1 = OK, 0 = violated; ro = selected rho parameter.
class Metric:

    def __init__(self, min, max, type, ro):
        self.min = min
        self.max = max
        self.type = type
        self.ro = ro


# instantiate metrics-> requirements. Nb: in check function are checked only the metrics
# belonging to user requirements.

response_time = Metric(0, 35, 1, 40)
latency = Metric(0, 2000, 1, 2000)
execution_time = Metric(0, 100, 1, 15)

throughput = Metric(1, 0, 0, 30000)
availability = Metric(90, 0, 0, 25)

# data consistency
d_c = Metric(0.4, 1, 0, 1 / k)


# function used to truncate floats
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


# function used to define numerically the impact of an action on a particular metric. delta= M(t+1)- M (t), ro=parameter for the metric
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
