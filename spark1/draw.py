import time
import os
import db
def border_msg(msg):

    count = len(msg) + 2

    dash = "-"*count

    print("+{}+".format(dash))

    print("| {} |".format(msg))

    print("+{}+".format(dash))


def draw():
    c=0
    r = db.lookup_data()
    c= c+1

    for row in r:
        if row [1] == 1:
           print ("Node 1")
           border_msg('X')
           print("id data set:"+ str(row[0]))
        elif row [1] == 2:
            print ("Node 2")
            border_msg('X')
            print("id data set:"+ str(row[0]))

        elif row [1] == 3:
             print ("Node 3")
             border_msg('X')
             print("id data set:"+ str(row[0]))

    time.sleep(5)
    if c <= 965 :
        os.system('cls')
        draw()


draw()
print ("finish")
draw()