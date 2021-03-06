This system simulates a distributed network of computing nodes, on which run applications consuming data (DaaS)  which rely on the same data source.
In order to simulate a distributed net of nodes far from each other, has been used a tool which injects latency among the nodes and the data source ([toxiproxy][proxy]).  
The computations consist in [Apache Spark][spark] applications, which calculate the average value of the cholesterol field of the provided data set, which consists in a large number of blood tests. The file containing the data set is stored in a [minIO server][minio], reachable from any application.
Through the proposed algorithm, the decision systems associated to the applications are capable of taking decisions (distributed control), in order to restore their QoS (Quality of Service) requirements at run-time in response to requirements violations.
The actions consists in data movement (MXY = move data from X to Y,  where  X and Y are the ID associated to the nodes of the net, i.e., 1, 2, ..), duplication actions (CXY = copy data from X to Y), and change reference copy actions (CRY =  change reference copy of the data set, to a data set located in resource Y ) toward the data set. 
The actions are guided by the knowledge of the impact that actions have on the metrics associated to the goal of the user (internal impacts).
The value of the metrics is measured by a monitoring program, associated to each application (distributed monitoring).

However, since the applications rely on the same data source, these actions can not be taken in complete isolation. To overcome this issue, has been developed a mechanism based on the release of external feedbacks on the performed actions in the environment, by the other involved applications (external impacts).

The algorithm uses some ML techiniques, and it is capable of adapting to the changes of the environment. Consequently, it is suitable for dynamic environments, as Fog Computing.

For the implementation, the applications and the tools used run in the form of containerized applications, based on built Docker IMGs.
An application is considered as composed by three main parts: the processing component (Spark computation), the decision system and the monitoring system. The latters (and in general all the logic behind the system) are implemented through Python programs which resides within the containers of the spark instances.  

In order to implement the algorithm and configure the environment and its properties, an instance of [mySQL server][mysql] is used, accessible from a [phpMyAdmin][dbgui] application.

The initial informations about the quality of the actions (internal impacts) are learned through an Offline Learning, executed through an automated program (training.py).

The provided distributed networks of nodes is composed by three nodes, identified by an ID (1, 2, 3), each of it hosting an application which has its own QoS requirements.
The selected QoS requirements of each applications are the following:

- Spark 1: Response time ≤ 35 s AND Availability ≥ 95%; 
- Spark 2: Throughput ≥ 30000 n/s AND Availability ≥ 80%;
- Spark 3: Data Consistency ≥ 0.7 OR Network Latency ≤ 1300 ms

However, it is possible to modify the thresholds associated to these metrics, by changing the values of min/max associated to the metrics in the 'metrics.py' file, located inside each of the spark folders.
The selected initial configuration is visible from the database GUI.
 

In the following are illustrated the steps to start the three applications, according to the proposed initial configuration. 



### Table of contents
- [Prerequisites:](#prerequisites)
- [Installation :](#installation-)
  * [Database setup (mySQL server + phpMyAdmin )](#database-setup-mysql-server--phpmyadmin-)
  * [Program setup](#program-setup)
  * [minIO server setup](#minio-server-setup)
  * [Initialization](#initialization)
- [Offline training(optional)](#offline-trainingoptional)
- [Usage](#usage)
- [Add other nodes to the network (without running applications)](#add-other-nodes-to-the-network-without-running-applications)
- [Add other applications to the system](#add-other-applications-to-the-system)


The following Figure shows the architecture of the system, after performing all the installation steps:
![](https://github.com/GiuMangiaracina/Thesis/blob/master/architecture%20.png)

Modifying the values from the GUI of the database, it is possible to change at run-time the properties of the environment, namely the availability (metadata associated to each node) and the latency (in ms)among the nodes.
Moreover, it is possible to change the initial configuration, or extend the network, adding both additional nodes and applications, following the instructions in the specific sections. In the latter cases, it is necessary to start the procedure from these sections, and the offline learning step must be executed, in order to setup properly the information about the initial impacts.

## Prerequisites:
- a working [Docker][docker] installation (for 64-bit systems);
- docker-compose installed  (to install it on Linux systems, type  ```sudo apt install docker-compose  ``` in the terminal.);
- for Linux users, xterm installed (to install it, type 'sudo apt-get install xterm' in the terminal.).
- if docker-machine is not installed in the same machine where it is installed docker CLI, for example for Windows users who use Docker Toolbox (legacy solution for Windows versions different from Windows 10 Professional and Enterprise 64-bit):
 1. determine the IP of your Docker virtual machine by running: 'docker-machine ip' after starting docker;
 2. start Oracle VM VirtualBox; locate the Docker virtual machine (usually named 'default'); select settings-> Network->Adapter1 (NAT) -> Advanced -> Portforwarding, then add the following rules (substitute the 'guest Ip' field with your docker-machine ip):
 ![](https://github.com/GiuMangiaracina/Thesis/blob/master/ports.JPG)
 
## Installation : 
Execute all the following instructions, in order.

- clone this repository to your working directory typing:  ``` git clone https://github.com/GiuMangiaracina/Thesis ```;
- extract in the working directory the compressed file 'file1.rar'.
### Database setup (mySQL server + phpMyAdmin )
1. move into 'db' directory. For Linux users, login as root user typing : ```sudo su ``` at the terminal;
2. build the images, typing: ```docker-compose build```;
3. start the containers, typing: ```docker-compose up &```;
4. access to phpMyAdmin web app browsing to 'http://127.0.0.1:8080';
5. login into database using the following credentials: 
 
 - system = MySql;
 - server = mysql-development;
 - username = root;
 - password = helloworld;
 - database = db;
 
6. import the database data and schemas from the provided dump file, clicking on Import-> File Upload -> Browse, and load the file 'db.sql', located in db/data/ . Then click on 'Execute'.
7. If you want to apply any edits to the initial configuration, edit the 'latency', 'availability', 'file_table' table values of the database from the GUI. The latter is used in order to set the initial position of the file, among the nodes.
   Otherwise skip this step.
  
### Program setup
In the 'program' directory:
1. build the containers, typing: ```docker-compose build```;
2. start the containers, typing ```docker-compose up &```.
This command will start the three applications, whose containers name are respectively : spark1, spark2 and spark3. Note that to each application is associated an ID (1,2,3) which corresponds both to the container name, and to the ID associated to the node where the application is considered running.

At any time, to login within each of the containers, type in the terminal the following command : ```docker exec -it sparkN bash```, substituting the value of N with the target container name (1, 2, 3, ..). To login simultaneously into the three containers, execute the start_bash_win.cmd or start_bash.sh program.


To verify in which containers you are, just type ``` ls ``` and verify the presence of an empty file among the files in the directory named 'SPARK N.txt', in which the N identifies the ID of the application.

### minIO server setup
1. Browse to 'http://127.0.0.1:9000', and login into minIO server instance using the following credentials: 
- username = minio ;
- password = minio123 .
2. Load the data set: click on the '+' button, below; create a bucket named 'miniobucket'; load the extracted file 'file1.json' into the bucket just created.

### Initialization
In the 'program' directory:

1. - for Windows users: execute 'start_win.cmd'and wait until its completion;
   - for Linux users: click on the file 'start.sh'and wait until its completion. Note that, at the end, a warning message may be shown. However, this should not cause concern.
    - for Mac users: execute 'start_mac.sh'and wait until its completion;
 This command initializes the proxies and the Spark History Servers.

After this initialization, the [Spark History Servers][history server] of the three applications, which show the details of the computations, are accessible at the following addresses:
- 'http://127.0.0.1:18081/' (Spark1);
- 'http://127.0.0.1:18082/' (Spark2);
- 'http://127.0.0.1:18083/' (Spark3);

## Offline training
The training step is used to produce the set of initial impact vectors, which represent the effects of the actions on the various QoS metrics.
 Since the applications contain already the output of the training (IMXY/ICXY/ICRY.txt text files), it is not necessary to re-execute the training program if the initial configuration is maintained (3 nodes and 3 applications). However, if big changes to the properties are executed (during the db setup step), or new nodes/applications are added, it is necessary to re-execute the training step. Moreover, since the computation performances may vary from a machine to another, is preferable to perform anyway this step.
 
 1. Execute the start_bash_win.cmd or start_bash.sh program in order to login within the three containers;
 2. (Optional)  type ``` nano training.py ``` and modify the constant N, to configure the number of iterations of the training step, namely the number of times each action is tried. The result stored in the impact vectors will be the average of the N steps. 
 3. In each of the terminals, type ``` python training.py ``` and wait until its completion. (Note that the required time can be quite long, depending on the number of nodes in the network and to the N value);
 4. in each of the terminals, type ``` cp -a /usr/spark-2.4.1/bin/output_training/. ./ ```, in order to copy the results of the training to the correct directory (/usr/spark-2.4.1/bin) . close the terminals.
 
Since the offline training can require a lot of time, you can store its output and just include it for the successive executions of the system. You can do it by coping in a local directory the folder containing the results:  ``` docker cp spark1:/usr/spark-2.4.1/bin/output_training ./ ``` 
then, copy all the .txt files into the corresponding spark directory, for example spark1 for the first instance. Overwrite all the eventually files with the same name with the newer. Apply this procedure for all the spark instances. Remember that the results of the training will be different from an application to another, because the applications are virtually placed in different nodes. Consequenly, you have to store the output files into the right directory corresponding to the application.
If you decide to store the vectors for reuse them, it is necessary to rebuilt the containers belonging to the folder 'program' in the next execution, in order to include the files within the containers. 

 
## Usage
In the 'program' directory, re-execute the following program:
- for Windows users:
execute 'start_win.cmd';
- for Linux users, once logged as root user (sudo su):
click on 'start.sh' .

- for Mac users: execute 'start_mac.sh';

This command starts the system, and executes in parallel the computations in an infinite loop, showing them on three different terminal windows.


During the execution, the events happened in the environment, namely the actions performed by the single decision systems and associated information, are posted and stored in the form of entry in the table 'events', visible through the phpMyAdmin application.

It is assumed that applications reach convergence when no new corrective actions are recorded, i.e. when application executions meet agreed requirements. At this point, it is possible to stop the computation, simply pressing ```ctrl+c``` in each of the terminal windows. 


To stop all the containers, once located from the terminal respectively in the 'program' and 'db' folders, type ``` docker-compose down``` .

## Add other nodes to the network (without running applications)
To add additional empty nodes to the network, i.e., without running applications, follow these instructions.
First of all, the nodes are identified by an ID, which for convention is an increasing number (1,2,3,..). In order to add nodes, you have to start from 4 onwards.

1. Follow the [database setup step](#database-setup-mysql-server--phpmyadmin-).
2. Go to 'spark1' folder and open the file 'add_nodes.py'. Go to the bottom of the file, and add new nodes. Each node needs to be created, added to the list of existing (1,2,3) nodes, and added to the system through the function add_node(ID).

The function add_node(ID), adds a node with id ID in the system. In particular, it adds to the 'latency' table all the possible combinations among the nodes in the network (present in the node_list), and the rows related to the availavilities values in the 'avaialability' table. 

For example, to add two nodes with ID 4 and 5 to the network, write below the node_list :
``` 
# add new nodes

N4 = Node(4, 1, 0, 0)
node_list.append(N4)
add_node(4)

N5 = Node(5, 1, 0, 0)
node_list.append(N5)
add_node(5)

``` 
In case you want to initialize randomly the latencies among the nodes, add to the end of the file this line:
``` 
initialize_random(node_list)
``` 

Execute the program by typing in a terminal this command: ``` docker exec -it spark1 python add_nodes.py ``` .

3. Go to tables 'latency' and 'availability' from the GUI of the database application, and fill in all the fields with value '-1' with the desired parameters.
Eventually, modify the other values in the tables.
In the 'latency' table, each row contains the mean latency in ms between each pair of nodes, identified by their unique ID (node_ID -> node).
Note that these are only averages values, since at run-time it is used a gaussian distribution with this mean and a large variance. For convention, set the values associated to the same pairs of nodes to the same values, in order to create symmetric properties. 
The availability properties (in percentage) are metadata associated to each node.
The following Figures show an example of configuration:


![](https://github.com/GiuMangiaracina/Thesis/blob/master/latency.PNG)
![](https://github.com/GiuMangiaracina/Thesis/blob/master/availability.PNG)

In this configuration, the added node with ID 4 has a mean latency of 2000 ms to node 1, of 1000 ms to node 2, of 500 ms to node 3 and finally of 200 ms to node 5.  Moreover, the node has a mean availability of 80 % .

4. Within each spark folder, open the file 'actions.py' and add the new nodes to the configuration, by adding these lines.
 ``` 
 # list of the available nodes in the net
 ..
 N4 = Node(4, 1, db.get_availability(4), db.get_latency(c_id, 4))
 N5 = Node(5, 1, db.get_availability(5), db.get_latency(c_id, 5))

 # add the nodes to the existing node list:
 node_list = [...., N4, N5] 
 ``` 
Note that the id of the applications corresponds to the value of the 'c_id' variable set in the 'actions.py' file.

5. Follow all the [Installation](#installation-) steps, excluding the setup of the database, that is already running.

6. Within each container, execute the training program, following the steps explained in [offline Training section](#offline-trainingoptional). Eventually store the results as explained in the section, for the next executions. If you have already the vectors, include them into the folders as exlplained in the section.

At this point you can start the program, following the [usage](#usage) section.

## Add other applications to the system
To add a new application to the system, it is necessary to add new files and configure them before to built the system.

Furthermore, it is necessary to add even an associated node to the system, where the application is virtually running.


Remembering that all the nodes are identified by an ID, with an increasing number (1,2,3,..). 
For convention, the associated applications have the same ID.
So, in order to add new applications and nodes, you have to start with an associated ID from 4 onwards. 
Follow these instructions (in general, you can use the previous 3 applications as guide, substituting the configuration with the right ID in the various files), for each of the new applications. When you read N, substitute with the correct ID (4, 5 ,...) value:

1.	duplicate a spark directory in the 'program' folder and rename it with 'sparkN'. Since each application have different requirements (you can read them above), you can duplicate the folder with the metrics of interest for the new application. Then you can modify the min/max thresholds changing the parameters in the 'metrics.py' file.


2. Open the 'docker-compose.yml' file in the 'program' folder, and add at the bottom the following lines for each new application, necessary to build the new container:
 ```
 sparkN:
        build : ./sparkN/
                 
        network_mode: host

        stdin_open : true

        tty : true
        
        container_name : sparkN
```


3. inside the folder 'sparkN', modify these values inside the various files, substituing N with the ID of the application:
-	In 'actions.py': 
```
 # controller id
 c_id = N 

 ```
 - in 'add.jon' :
  ```
    {
    "name": "minioProxyN",
    "listen": "127.0.0.1:800N",
    "upstream": "127.0.0.1:9000",
    "enabled": true
  }
   ```
-	in 'app.sh': 
``` { time spark-submit --master local[2] --conf spark.hadoop.fs.s3a.endpoint=http://127.0.0.1:800N script.py 2>1 ;} 2>> time.log ```

- in	'db.py' :
1.set variable 'N' to the total number of applications.

2. inside the feedback(t_viol) function, in the lines below substitute N with the ID of the application: 
``` 
def feedback(t_viol):
    ...
        sql2 = "update events set sum_feedback = sum_feedback + %s  where id = % s and feedback_N = 0"
        sql1 = "update events set feedback_N = %s where id = % s and feedback_N = 0"
    ...
   
```
- in 'set.sh': 
``` curl -X POST http://127.0.0.1:8474/proxies/minioProxyN/toxics -d "@template.json" ```

- in 'spark-defaults.conf', modify the following lines:

``` ...
    spark.hadoop.fs.s3a.endpoint=http://127.0.0.1:800N
    spark.history.ui.port=1808N 
```
- in 'modify.sh' :
```  
curl -X POST http://127.0.0.1:8474/proxies/minioProxyN/toxics/latency -d "@template.json"
```
modify the file which starts the applications (start.sh or start_win.cmd), in order to add even the new created one. For example, for start.sh, add at the end:
```
xterm -e docker exec -it sparkN python init.py &
```
Do the same thing for the files start_bash.sh (or start_win_bash.cmd), adding the line corresponding to the new application.


At this point, you can follow the steps of the [add nodes section](#add-other-nodes-to-the-network-without-running-applications), and, when you had setup the database, after the import of the dump file, you must add a column named 'feedback_N' of type dobule to the 'events' table in the database for each new application, through the database GUI.
Follow the example of the other feedbacks column of the table.
Remember that for each application, it is necessary to add the node with the same ID. So, for example, if you want to add another application in addition to the three existing, its ID will be 4, and the associated ID of the node will be 4.


The [offline training step](#offline-trainingoptional) must be executed.

For the usage, note what said for the other applications, just substitute the ID value with the right one. For example, given an application with ID 4, its Spark History Server will be accessible from the address: 'http://127.0.0.1:18084' .


[proxy]: https://github.com/Shopify/toxiproxy
[minio]: https://min.io/
[spark]: https://spark.apache.org/
[history server]: https://spark.apache.org/docs/latest/monitoring.html
[docker]: https://docs.docker.com/get-docker/
[mysql]: https://www.mysql.com/it/
[dbgui]: https://www.phpmyadmin.net/
