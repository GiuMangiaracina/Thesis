import pymysql
import random

connection = pymysql.connect(host='127.0.0.1', user='root', port=3308, password='helloworld', db='db', autocommit=True)


class Node:
    def __init__(self, id, disk, availability, mean_delay):
        self.id = id
        self.disk = disk
        self.availability = availability
        self.mean_delay = mean_delay


def update_latency(node_id, node_target, value):
    global connection
    cur = connection.cursor()

    sql = "update latency set value = %s where node_ID=%s and node=%s"
    s = (value, node_id, node_target)
    cur.execute(sql, s)
    connection.commit()
    cur.close()



# method used to update the availability of a given node
def update_availability(node_id, value):
    global connection
    cur = connection.cursor()
    sql = "update availability set value = %s where node=%s"
    s = (value, node_id)
    cur.execute(sql, s)
    connection.commit()
    cur.close()

def add_node(node_id):
    # add missing latencies between nodes -> fill in manually all the -1 values manually from the db GUI!
    global connection, node_list
    cur = connection.cursor()

    sql2 = 'SELECT COUNT(*) FROM latency WHERE node_ID = %s'
    x = (node_id)
    cur.execute(sql2, x)
    m = cur.fetchone()[0]

    if m == 0:

        sql = 'insert into latency (node_ID,node,value) values (%s,%s,%s)'
        s = (node_id, node_id, 0)
        cur.execute(sql, s)
        for a in node_list:

            if a.id != node_id:
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


def initialize_random(node_list):
    global connection
    cur = connection.cursor()

    # initialize random latencies among nodes
    for n in node_list:
        for m in node_list:
            if m.id != n.id:
                r = random.randint(100, 2000)
                update_latency(n.id, m.id, r)
                update_latency(m.id, n.id, r)

    # initialize random availability
    for m in node_list:
        r = random.randint(60, 99)
        update_availability(m.id, r)

    connection.commit()
    cur.close()
    print("Network initialized.")


# define the nodes to add to the list
N1 = Node(1, 1, 0, 0)
N2 = Node(2, 1, 0, 0)
N3 = Node(3, 1, 0, 0)


node_list = [N1, N2, N3]

# add new nodes
N4 = Node(4, 1, 0, 0)
node_list.append(N4)
add_node(4)

N5 = Node(5, 1, 0, 0)
node_list.append(N5)
add_node(5)

N6 = Node(6, 1, 0, 0)
node_list.append(N6)
add_node(6)

N7 = Node(7, 1, 0, 0)
node_list.append(N7)
add_node(7)

N8 = Node(8, 1, 0, 0)
node_list.append(N8)
add_node(8)

N9 = Node(9, 1, 0, 0)
node_list.append(N9)
add_node(9)

N10 = Node(10, 1, 0, 0)
node_list.append(N10)
add_node(10)

#initialize_random(node_list)
