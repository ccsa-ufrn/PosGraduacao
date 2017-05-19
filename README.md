# Minerva

## About

Utility system for the workers and students of the postgraduate programs at Applied Social 
Sciences Center (CCSA) in Universidade Federal do Rio Grande do Norte (UFRN).

License: [GPL 3](./LICENSE).

## Setting up development environment (using Linux Ubuntu 17.04)
### First of all: configuring development files

Start by cloning this repository in a local folder and change directory to it.

Settig up our silly security file. Open ```Minerva/MinervaEnv/Minerva/fake/api_keys.json``` using your 
favorite text/code editor, copy its content without comments (by the way, read them) 
and paste at ```./MinervaEnv/Minerva/env/api_keys.json```.
A suggestion that may work (note that I use ```nano``` editor, but it's a personal option):

```sh
cd MinervaEnv/Minerva/
mkdir .env/ # create directory
touch .env/api_keys.json # create an empty file
cat ./fake/api_keys.json > ./env/api_keys.json # copying a model 
nano ./env/api_keys.json # open text editor for this file
# at editing its content, remove ALL COMMENT LINES
# also, if you know valid authorization datas for putting here... then do it!
```

That's it.

Now choose between two installation recipes: using VirtualEnv or Docker.

### ... VirtualEnv way.

Having already installed:
  - Python 3.5 interpreter, ```python3``` (was already installed by default)
  - PyPI 9 client, ```pip3``` from 'python3-pip' package (usual ```sudo apt install``` command)
  - VirtualEnv module, ```python3 -m virtualenv``` command (usual ```sudo pip3 install``` script)
  - MongoDB 3.2 and its shell ```mongo``` from an updated source (following [this Digital Ocean tutorial](https://www.digitalocean.com/community/tutorials/como-instalar-o-mongodb-no-ubuntu-16-04-pt))

Use these command lines to create and activate the virtual environment:

```sh
cd ./MinervaEnv/
python3 -m virtualenv ./
source ./bin/activate
```

You will notice a ```(Minerva)``` prefixing your prompt string if it worked.
Now install all required libs:

```sh
$ pip install -r ./requirements.txt
```

After that, let's start a mongo service. Here, in my poor Ubuntu, I run:

```sh
sudo systemctl start mongod
sudo systemctl status mongod
```

And then I see, while running status operation, an output "Active: active (running)".

Assuming that there's no Minerva database installed, it's necessary to run a initial script for inputting
some initial data.
Consists of redirecting the content from a json to ```mongo``` shell input:

```sh
cd ../dev_db/
mongo < ./standard_installation.js
cd ../MinervaEnv
```

Please, check if mongo output looking for errors before proceding. Make sure to have an updated
Mongo service running.

If packages installation went successfully and our configuration files are ok, you can
now start running the local server:

```sh
python app.py
```

Assuming that you did everything right, your terminal will output the URL for you to access using a web browser.
It should be http://localhost:4444/ but always read the output ("0.0.0.0:80" means you have super user
permission and your server it's opened for public access, so you need to know your IP address instead of "localhost" or "0.0.0.0").

You should see the application running locally now. Any doubts, just open an issue here on GitHub!

### ... Docker way.

Having already installed:
  - ```docker``` from 'docker-engine' package (I had to follow [this @caleblloyd's workaround](https://github.com/moby/moby/issues/32423))
  - ```docker-compose``` from its homonym PyPI module (usual ```sudo pip3 install``` command globally)

Just git clone this repository. change directory to it. Make sure to have Docker deamon running (```systemctl status docker``` should show its current status, maybe needing a ```sudo``` prefixing it)

Again change directory, now to MinervaEnv folder. Then, use ```docker-compose``` there:

```sh
cd MinervaEnv/
sudo docker-compose up -d # it may take a while, go get a coffe or something
# (the '-d' will make it run in background)
```

If everything went ok, both Flask and Mongo will be running in your machine, the server should be available
for your whole local network. Use ```ifconfing``` to find your IP and type it on browser.

But before accessing it in your browser, just feed Mongo image with some standard data
(assuming you're still in MinervaEnv directory):
```sh
# This command will send installation.js content to a mongo service running in minervaenv_db_1 container
sudo docker exec -i minervaenv_db_1 mongo < ../dev_db/standard_installation.js 
```

This should do the trick. Use your browser now.
