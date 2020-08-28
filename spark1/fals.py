import numpy as np
import  actions
import metrics
from init import computation

#5 times from n3
print ("from n3 2 times")
for k in range(1,3,1):

#actions.N3.availability=70
    actions.N3.mean_delay=1200
    actions.update_state(actions.N3)
    computation(actions.state)

print ("from n3 ")
for k in range(1,2,1):
    actions.N3.mean_delay=1500
    actions.update_state(actions.N3)
    computation(actions.state)

print ("from n2 changed")
actions.update_state(actions.N2)
computation(actions.state)
actions.N2.availability=78
actions.N2.mean_delay=800

print ("from n2 3 times")
#5 times from 0
for k in range(1,2,1):
    actions.update_state(actions.N2)
    computation(actions.state)


actions.N2.mean_delay=1300
actions.N1.disk=1
print ("from n2 1 times 1300")
actions.update_state(actions.N2)
computation(actions.state)
print ("change lat 2 to 800")
print ("change av 2 to 78")
actions.N2.availability=78
actions.update_state(actions.N2)
computation(actions.state)

print ("from n3 4 times, n1 not available and 1400 n3")
for k in range(1,5,1):
    actions.N1.disk=0
    actions.N3.mean_delay=1400
    actions.update_state(actions.N3)
    computation(actions.state)' >> z.py


echo 'import actions
import metrics
import numpy as np
from init import computation
for k in range(1,5,1):
    actions.N3.availability=75
    actions.N3.mean_delay=400
    actions.update_state(actions.N3)
    computation(actions.state)' >> r.py















