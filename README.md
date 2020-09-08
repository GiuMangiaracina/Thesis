This system simulates a distributed network of resources, on which are running applications consuming data (DaaS) relying on the same data source. Through the proposed algorithm, the applications apply distributed control, in order to guarantee their QoS requirements at run-time, in response to requirements violations.
## Prerequisities:
- A working Docker installation (for 64-bit systems);
- docker-compose installed  (to install it on Linux systems, type 'sudo apt install docker-compose' in the terminal.);
- for Linux users, xterm installed (to install it, type 'sudo apt-get install xterm' in the terminal.).
- for Windows users using Docker Toolbox (legacy solution for Windows versions different from Windows 10 Professional and Enterprise 64-bit.):
 1. determine the IP of your Docker virtual machine by running: 'docker-machine ip' after starting docker;
 2. start Oracle VM VirtualBox, locate the Docker virtual machine (usually named 'default') and select settings-> Network->Adapter1 (NAT) -> Advanced -> Portforwarding and add the following rules (substitute the guest Ip field with your docker machine ip):
 ![](https://github.com/GiuMangiaracina/Thesis/blob/master/ports.JPG)
 
## Instruction : 
Execute the following instructions in order.

- clone this repository to your working directory typing 'git clone https://github.com/GiuMangiaracina/Thesis';
- extract in the working directory the compressed file  'file1.rar'.
### Database setup (mySQL server + phpMyAdmin )
1. move into  db directory. For Linux users, login as root user typing 'sudo su' at the terminal;
2. build the images, typing 'docker-compose build';
3. start the containers, typing 'docker-compose up';
4. access to phpMyAdmin web app browsing to 'https://127.0.0.1/8080';
5. login into database using the following credentials: 
 - system = MySql;
 - server = mysql-development;
 - username = root;
 - password = helloworld;
 - database = db;
6. import the database, clicking on Import-> File Upload -> Browse, and load the file 'dump_db.sql', located in db/data/ . Then click on 'Execute'.
### Program setup
In the program directory:
1. build the containers, typing 'docker-compose build';
2. start the containers, typing 'docker-compose up'.
### minIO server setup
1. Browse to 'https://127.0.0.1/9000', and login into minIO server instance using the following credentials: 
- username = minio;
- password = minio123 .
2. load the json file: click on the '+' button, below; create a bucket named 'miniobucket'; load the extracted file 'file1.json' into the bucket just created.

### Initialization (this command, executed for the first time, initializes the proxies and the history servers.)
In the program directory:

- for Windows users: execute 'start_win.cmd';
- for Linux users: 
1. execute 'permission.sh'
2. execute 'start.sh'.
## Usage (this command executes in parallel the three computations.)
In the program directory:
- for Windows users:
execute 'start_win.cmd';
- for Linux users:
1. execute 'permission.sh';
2. execute 'start.sh' .
