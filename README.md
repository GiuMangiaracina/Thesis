This system simulates a distributed network of resources, on which are running applications consuming data (DaaS) relying on the same data source.
The computations consist in Spark applications, which calculate the average value of a field of the provided data set. 
Through the proposed algorithm, the applications apply distributed control, in order to guarantee their QoS requirements at run-time, in response to requirements violations.
## Prerequisities:
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
- extract in the working directory the compressed file  'file1.rar'.
### Database setup (mySQL server + phpMyAdmin )
1. move into  db directory. For Linux users, login as root user typing 'sudo su' at the terminal;
2. build the images, typing 'docker-compose build';
3. start the containers, typing 'docker-compose up';
4. access to phpMyAdmin web app browsing to 'http://127.0.0.1/8080';
5. login into database using the following credentials: 
 - system = MySql;
 - server = mysql-development;
 - username = root;
 - password = helloworld;
 - database = db;
6. import the database, clicking on Import-> File Upload -> Browse, and load the file 'dump_db.sql', located in db/data/ . Then click on 'Execute':
7. eventually apply any edits to the initial configuration, editing the tables of the database.
### Program setup
In the program directory:
1. build the containers, typing 'docker-compose build';
2. start the containers, typing 'docker-compose up'.
### minIO server setup
1. Browse to 'http://127.0.0.1:9000', and login into minIO server instance using the following credentials: 
- username = minio;
- password = minio123 .
2. load the json file: click on the '+' button, below; create a bucket named 'miniobucket'; load the extracted file 'file1.json' into the bucket just created.

### Initialization (this command, executed for the first time, initializes the proxies and the history servers.)
In the program directory:

- for Windows users: execute 'start_win.cmd';
- for Linux users: 
1. execute 'permission.sh' (needed to obtain the permissions to excute the files within the containers);
2. execute 'start.sh' and wait until its completion.

After this initialization, the Spark History Servers of the three applications are accessible at the following addresses:
- 'http://127.0.0.1:18080' (spark1)
- 'http://127.0.0.1:18081' (spark2)
- 'http://127.0.0.1:18082' (spark3)
## Usage (this command starts the system, and execute in parallel the computations.)
In the program directory, rerun the following command:
- for Windows users:
execute 'start_win.cmd';
- for Linux users:
execute 'start.sh' .
