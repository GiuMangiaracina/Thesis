# function used to add a node with id ID in the environment. After executing it, go to table 'latency' and 'availability' of the database to fill in the fields with value '-1' with the parameters.


import db
db.add_node(4)