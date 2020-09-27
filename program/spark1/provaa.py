
# function used to add a node with id ID in the db. then, go to table 'latency' and 'availability' to fill in the fields with value '-1' with the parameters.
#db.add_node(4)

# function to generate actions
#import actions
import db
#actions.generate_actions(actions.node_list)

#for a in actions.action_list:
#	print(a.source)

#db.fill_in_gpw()

c=db.check_gpw_table()

print(str(c))