# Thesis
## Prerequisities:
- A working Docker installation;
- for Linux users, xterm (to install it, type 'sudo apt-get install xterm' in the terminal.
- for Windows users using Docker Toolbox (legacy solution for Windows versions different from Windows 10 Professional and Enterprise 64-bit.):
 1. determine the IP of your Docker virtual machine by running: 'docker-machine ip' after starting docker;
 2. Start Oracle VM VirtualBox, locate the Docker virtual machine (usually named 'default') and select settings-> Network->Adapter1 (NAT) -> Advanced -> Portforwarding and add the following rules (substitute the guest Ip field with your docker machine ip):
 ![alt text](https://github.com/GiuMangiaracina/Thesis/ports.jpg)
 
## Instruction : 
Execute the following instruction in order.

- Clone this repository to your working directory typing 'git clone https://github.com/GiuMangiaracina/Thesis';
- extract in the working directory the compressed file  'file1.rar'.
### Database setup
1. move into  db directory. For Linux users, login as root user typing 'sudo su' at the terminal;
2. type 'docker-compose build';
3. type 'docker-compose up';
4. access to mySQL php administrator web app browsing to 'https://127.0.0.1/8080';
5. login into database using the following credentials: 
 - system = MySql;
 - server = mysql-development;
 - username = root;
 - password = helloworld;
 - database = db;
6. import the database, clicking on Import-> File Upload -> Browse and load the file 'dump_db.sql', located in db/data/ . Then click on 'Execute'.
### Program setup
In program diretory:
1. type 'docker-compose build';
2. type 'docker-compose up'.
### minIO setup
1. Browse to 'https://127.0.0.1/9000' and login using the following credentials: 
- username = minio;
- password = minio123 .
2. load the json file: click on the '+' button, below; create a bucket named 'miniobucket'; load the extracted file 'file1.json' into the bucket just created.

### Initialization (this command, executed for the first time, initializes the proxies and the history servers.)
In program directory:

- for Windows users: execute 'start_win.cmd';
- for Linux users: 
1. execute 'permission.sh'
2. execute 'start.sh'.
### Usage (this command executes in parallel the three computations.)
In program directory:
- for Windows users:
execute 'start_win.cmd';
- for Linux users:
1. execute 'permission.sh';
2. execute 'start.sh' .
