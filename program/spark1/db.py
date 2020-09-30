import pymysql
from time import time
import threading
import actions
import math

# time windows, measured in seconds
T = 210

# number of applications
N = 3

threshold = 0.3

# create connection to connect to the database
connection = pymysql.connect(host='127.0.0.1', user='root', port=3308, password='helloworld', db='db', autocommit=True)


'''
# method used to add controller

def get_id():
    global connection
    cur = connection.cursor()
    sql = "INSERT INTO controller_id VALUES()"

    cur.execute(sql)
    connection.commit()
    sql2 = "SELECT LAST_INSERT_ID()"
    cur.execute(sql2)
    c = cur.fetchone()[0]
    cur.close()
    actions.update_c_id(c)
'''

# method used to insert action event on db
def insert_action(action, random):
    global connection
    cur = connection.cursor()
    sql1 = "INSERT INTO events (data_source,action,time_stamp,active,controller_id,random,action_type) VALUES (%s,%s,%s,%s,%s,%s,%s)";
    t = int(time())
    print("time_stamp:" + str(t))
    if action.id != 0:
        s = (actions.data_set_id, action.id, t, 1, actions.c_id, random, action.type)
    else:
        s = (actions.data_set_id, action.id, t, 0, actions.c_id, random, action.type)
    cur.execute(sql1, s)
    connection.commit()
    sql2 = "SELECT LAST_INSERT_ID()"
    cur.execute(sql2)
    r = cur.fetchall()
    cur.close()
    print("PUBLISHED EVENT, id:" + str(r))
    return r


# methods used to close temporal window on db after T is expired
# (delayed function)
def close_t(event_id):
    global connection
    cur = connection.cursor()
    sql = "update events set active = 0 where id= %s "
    r = (event_id)
    cur.execute(sql, r)
    connection.commit()
    print("\n")
    print("CLOSED T of event " + str(event_id))
    update_counter(event_id)
    cur.close()


def close_T(event_id):
    global T
    print("..START WAITING..")
    timer = threading.Timer(T, close_t, args=(event_id))
    timer.start()


# method used to leave negative feedback p

def feedback(t_viol):
    global connection, T
    cur = connection.cursor()
    sql = "select time_stamp,id from events where active = 1 and controller_id != %s and action != 0 and data_source= %s "
    cur.execute(sql, (actions.c_id, actions.data_set_id))
    rows = cur.fetchall()
    if cur.rowcount == 0:
        print("No open events.")

    else:
        for row in rows:
            ts = row[0]
            event_id = row[1]
        # compute negative feedback
            p = 1 - ((t_viol - ts) / T)

        # write negative feedback into event entry

            sql2 = "update events set sum_feedback = sum_feedback + %s  where id = % s and feedback_1 = 0"
            q = (p, event_id)
            cur.execute(sql2, q)
            connection.commit()
            sql1 = "update events set feedback_1 = %s where id = % s and feedback_1 = 0"
            r = (p, event_id)
            cur.execute(sql1, r)
            connection.commit()

        print("FEEDBACK LEFT: " + str(p))
        print("\n")
    cur.close()


# method used to read global counter
def read_counter(action):
    global connection
    cur = connection.cursor()
    sql = "select value from global_counter where id = %s"
    s = (action.id)
    cur.execute(sql, s)
    c = cur.fetchone()[0]
    cur.close()
    return c


# method used to update global counter
def update_counter(event_id):
    global connection, N, threshold
    cur = connection.cursor()

    # compute global feedback

    sql = "select sum_feedback,action from events where id=%s "
    r = (event_id)
    cur.execute(sql, r)
    row = cur.fetchone()

    global_feedback = (row[0]) / (N - 1)
    global_feedback = truncate(global_feedback, 2)

    print("global feedback: " + str(global_feedback))

    sql1 = "select value from global_counter where id=%s"
    r = (row[1])
    cur.execute(sql1, r)
    value = cur.fetchone()

    print("previous value = " + str(value))

    # increment counter
    if global_feedback >= threshold:

        sql2 = "update global_counter set value=%s where id = %s "
        z = (value[0] + 1, row[1])
        cur.execute(sql2, z)
        connection.commit()
        print("global feedback >= fixed threshold (" + str(threshold) + ")")
        print("UPDATED COUNTER VALUE :++ " + str(value[0] + 1))
    else:
        if value[0] != 0:
            # decrement counter

            sql3 = "update global_counter set value=%s where id = %s "
            h = (value[0] - 1, row[1])
            cur.execute(sql3, h)
            connection.commit()
            print("global feedback < fixed threshold (" + str(threshold) + ")")
            print("UPDATED COUNTER VALUE :-- " + str(value[0] - 1))
        else:
            print("counter not updated (0)")

    cur.close()


# method used to update the position of a data set
def update_data(id, node):
    global connection
    cur = connection.cursor()
    sql = "update file_table set node = %s where data_set = % s"
    s = (node, id)
    cur.execute(sql, s)
    connection.commit()
    cur.close()


# method used to retrieve the position of a data set
def set_data(id):
    global connection
    cur = connection.cursor()
    sql = "select node from file_table where data_set = % s"
    s = (id)

    cur.execute(sql, s)
    connection.commit()
    value = cur.fetchone()
    cur.close()
    return value[0]


# method used to create a new data set
def add_data(id):
    global connection
    cur = connection.cursor()
    sql = "INSERT INTO file_table (node) VALUES (%s)"
    s = (id)
    cur.execute(sql, s)
    connection.commit()

    sql1 = "SELECT LAST_INSERT_ID()"
    cur.execute(sql1)
    r = cur.fetchone()[0]
    cur.close()
    return r


# this method returns the file_table content
def lookup_data():
    global connection
    cur = connection.cursor()
    sql = "select * from file_table "

    cur.execute(sql)
    value = cur.fetchall()
    connection.commit()
    cur.close
    return value


# method used to lock the computation
def lock_computation():
    global connection
    cur = connection.cursor()
    sql = "update computation_lock set Locked = 1"
    cur.execute(sql)
    connection.commit()

    print("resource acquired")
    cur.close()


# method used to unlock the computation
def unlock_computation():
    global connection
    cur = connection.cursor()
    sql = "update computation_lock set Locked = 0"
    cur.execute(sql)
    connection.commit()
    print("resource released")
    cur.close()


# method used to check the status of the computation (lock)
def check_computation():
    global connection
    cur = connection.cursor()
    sql = "select Locked from computation_lock"
    cur.execute(sql)
    connection.commit()

    r = cur.fetchone()[0]
    cur.close()
    return r


# method used to update the availability of a given node
def update_availability(node_id, value):
    global connection
    cur = connection.cursor()
    sql = "update availability set value = %s where node=%s"
    s = (value, node_id)
    cur.execute(sql, s)
    connection.commit()
    cur.close()


# method used to retrieve the availability value of a given node
def get_availability(node_id):
    global connection
    cur = connection.cursor()
    sql = "select value from availability where node = %s"
    s = (node_id)
    cur.execute(sql, s)
    connection.commit()
    r = cur.fetchone()[0]

    return r


# method used to count the number of existing copies of a data set
def check_dc():
    global connection
    cur = connection.cursor()
    sql = "SELECT COUNT(*) from events where data_source =%s and action_type = 'copy'"
    s = (actions.data_set_id)
    cur.execute(sql, s)
    connection.commit()
    r = cur.fetchone()[0]
    cur.close()
    return r


# this method returns the latency from a node with id =c_id and the node with id node_id
def get_latency(c_id, node_id):
    global connection
    cur = connection.cursor()
    sql = "select value from latency where node=%s and node_ID=%s"
    s = (node_id, c_id)
    cur.execute(sql, s)
    connection.commit()
    r = cur.fetchone()[0]
    return r


# this method updates the latency from a node with id =c_id and the node with id node_id
def update_latency(node_id, node_target, value):
    global connection
    cur = connection.cursor()

    sql = "update latency set value = %s where node_ID=%s and node=%s"
    s = (value, node_id, node_target)
    cur.execute(sql, s)
    connection.commit()
    cur.close()


def add_node(node_id):
    # add missing latencies between nodes -> fill in manually all the -1 values manually from the db GUI!
    global connection
    cur = connection.cursor()

    sql2 = 'SELECT COUNT(*) FROM latency WHERE node_ID = %s'
    x = (node_id)
    cur.execute(sql2, x)
    m = cur.fetchone()[0]

    if m == 0:

        sql = 'insert into latency (node_ID,node,value) values (%s,%s,%s)'
        s = (node_id, node_id, 0)
        cur.execute(sql, s)
        for a in actions.node_list:
            sql = 'insert into latency (node_ID,node,value) values (%s,%s,%s)'
            s = (node_id, a.id, -1)
            cur.execute(sql, s)
            sql1 = 'insert into latency (node_ID,node,value) values (%s,%s,%s)'
            s = (a.id, node_id, -1)
            cur.execute(sql1, s)
        connection.commit()
    print("Node with ID " + str(
        node_id) + " added. Please add the node to the node list, and fill in the -1 values in the database.")

    # add availability node-> -1 to fill in

    sql2 = 'insert into availability (node, value) values (%s,%s)'
    p = (node_id, -1)
    cur.execute(sql2, p)
    connection.commit()
    cur.close()


def fill_in_gpw():
    global connection
    cur = connection.cursor()
    for a in actions.total_action_list:
        sql = 'insert into global_counter (action,id,value) values (%s,%s,%s)'
        p = (a.label, a.id, 0)
        cur.execute(sql, p)
        connection.commit()
    cur.close()


def check_gpw_table():
    global connection
    cur = connection.cursor()

    sql = 'SELECT EXISTS (SELECT 1 FROM global_counter);'

    cur.execute(sql)

    code = cur.fetchone()[0]
    cur.close()
    return code


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


if __name__ == "__main__":
    __main__()
