import db
import actions
from init import computation

def setting():
    n = db.set_data(actions.data_set_id)

    actions.set_state(n)

    computation(actions.state)

