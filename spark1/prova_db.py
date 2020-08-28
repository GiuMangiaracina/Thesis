
import threading
import time
import actions
import metrics
import db
import actions
import random
import numpy as np

from init import check
#event_id=db.insert_action(M31)

#print(str(event_id))

#db.close_T(event_id)
#c=db.read_counter(M31)
#print (c)
#d=c+1
#print (d)

#db.update_counter(177)
#score=0.6
#penalty_factor=0.3
#c = db.read_counter(M31)
#score_p = score * (1-penalty_factor * c)
#print (score_p)
#db.feedback(int(time()))

#n= db.set_data(actions.data_set_id)
#print (str(n))

#db.update_data(1,2)
#db.add_data(1)

#print (str(actions.data_set_id))
#actions.update_data_set(3)
#print (str(actions.data_set_id))

#selected=actions.C13

#if selected.type == "move":
 #  db.update_data(actions.data_set_id,selected.destination.id)

#elif selected.type == "copy":
 #    id= db.add_data(7)
 #    actions.update_data_set(id)
  #   print (actions.data_set_id)
#db.feedback(int(time()))
#db.unlock_computation()
#db.lock_computation()


#while db.check_computation():
 #     print ("wait your turn")


#db.lock_computation()

#db.unlock_computation()


#while db.check_computation():
 #   print ("wait your turn")

#r=db.get_availability(2)
#print (r)

#db.update_availability(2,50)



check(60,24,4000,200,actions.N2)






