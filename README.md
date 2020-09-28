This system simulates a distributed network of resources, on which are running applications consuming data (DaaS) relying on the same data source.
In order to simulate a distributed net of nodes far from each other, has been used a tool which injects latency among the nodes (toxiproxy https://github.com/Shopify/toxiproxy).
The computations consist in Apache Spark applications (https://spark.apache.org/), which calculate the average value of the cholesterol field of the provided data set, which consists in a large number of blood tests. The file containing the data set is stored in a minIO server (https://min.io/), reachable from any application.
Through the proposed algorithm, the decision systems associated to the applications are capable of taking decisions (distributed control), in order to restore their QoS requirements at run-time in response to requirements violations.
The actions consists in data movement, duplication actions, and change reference copy actions toward the data set. 
The actions are guided by the knowledge of the impact that actions have on the metrics associated to the goal of the user (internal impacts).
The value of the metrics is measured by a monitoring program, associated to each application (distributed monitoring).

However, since the applications rely on the same data source, these actions can not be taken in complete isolation. To overcome this issue, has been developed a mechanism based on the release of external feedbacks on the performed actions in the environment, by the other involved applications (external impacts).

The algorithm uses some ML techiniques, and it is capable of adapting to the changes of the environment. Consequently, it is suitable for dynamic environments, as Fog Computing.

The applications and the tools used run in the form of containerized applications, based on Docker containers.

In order to implement the algorithm and configure the environment and its properties, an instance of a mySQL database server is used, accessible from a phpMyAdmin application.

The initial informations about the quality of the actions (internal impacts) are learned through an Offline Learning, executed through an automated program .

The distributed networks of nodes is composed by three nodes, each of it hosting an application which has its own QoS requirements. In the following are illustrated the steps to start the three applications, according to the chosen initial configuration. 
Modifying the values of the database, it is possible to change at run-time the properties of the environment, namely the availability and the latency among the nodes.
However, it is possible to change the initial configuration, or extend the network, adding both additional nodes and applications, following the instruction in the attached document [?]. In the latter cases, the offline learning must be executed, in order to setup properly the information about the initial impacts.

## Prerequisites:
- a working docker installation (for 64-bit systems); (https://docs.docker.com/get-docker/)
- docker-compose installed  (to install it on Linux systems, type 'sudo apt install docker-compose' in the terminal.);
- for Linux users, xterm installed (to install it, type 'sudo apt-get install xterm' in the terminal.).
- for Windows users which use Docker Toolbox (legacy solution for Windows versions different from Windows 10 Professional and Enterprise 64-bit):
 1. determine the IP of your Docker virtual machine by running: 'docker-machine ip' after starting docker;
 2. start Oracle VM VirtualBox; locate the Docker virtual machine (usually named 'default'); select settings-> Network->Adapter1 (NAT) -> Advanced -> Portforwarding, then add the following rules (substitute the 'guest Ip' field with your docker-machine ip):
 ![](https://github.com/GiuMangiaracina/Thesis/blob/master/ports.JPG)
 
## Installation : 
Execute all the following instructions, in order.

- clone this repository to your working directory typing 'git clone https://github.com/GiuMangiaracina/Thesis';
- extract in the working directory the compressed file 'file1.rar'.
### Database setup (mySQL server + phpMyAdmin )
1. move into db directory. For Linux users, login as root user typing 'sudo su' at the terminal;
2. build the images, typing 'docker-compose build';
3. start the containers, typing 'docker-compose up';
4. access to phpMyAdmin web app browsing to 'http://127.0.0.1/8080';
5. login into database using the following credentials: 
 - system = MySql;
 - server = mysql-development;
 - username = root;
 - password = helloworld;
 - database = db;
6. import the database data and schemas from the provided dump file, clicking on Import-> File Upload -> Browse, and load the file 'dump_db.sql', located in db/data/ . Then click on 'Execute':
7. eventually apply any edits to the initial configuration, editing the 'latency' and 'availability' tables of the database.
### Program setup
In the program directory:
1. build the containers, typing 'docker-compose build';
2. start the containers, typing 'docker-compose up'.
### minIO server setup
1. Browse to 'http://127.0.0.1:9000', and login into minIO server instance using the following credentials: 
- username = minio ;
- password = minio123 .
2. load the data set: click on the '+' button, below; create a bucket named 'miniobucket'; load the extracted file 'file1.json' into the bucket just created.

### Initialization (this command, executed for the first time, initializes the proxies and the history servers.)
In the program directory:

- for Windows users: execute 'start_win.cmd'and wait until its completion;
- for Linux users, once logged as root user: 
1. execute 'permission.sh' (needed to obtain the permissions to excute the files within the containers);
2. execute 'start.sh'and wait until its completion.

After this initialization, the Spark History Servers (https://spark.apache.org/docs/latest/monitoring.html) of the three applications, which shows the properties of the computations, are accessible at the following addresses:
- 'http://127.0.0.1:18080' (spark1)
- 'http://127.0.0.1:18081' (spark2)
- 'http://127.0.0.1:18082' (spark3)
## Usage (this command starts the system, and execute in parallel the computations, showing them on three different terminal windows.)
In the program directory, rerun the following command:
- for Windows users:
execute 'start_win.cmd';
- for Linux users:
execute 'start.sh' .


The events happened in the environment, namely the actions performed by the single decision systems and associated information, are posted and stored in the form of entry in the table events, visible through the phpMyAdmin application.


It is assumed that applications reach convergence when no new corrective actions are recorded, i.e. when application executions meet agreed requirements. At this point, it is possible to stop the computation, simply pressing ctrl+c in each of the terminals. 
