import db
import actions

actions.generate_actions(actions.node_list)
db.fill_in_gpw()