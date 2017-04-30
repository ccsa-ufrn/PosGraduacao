# Minerva

## About

Utility system for the workers and students of the postgraduate programs at Applied Social 
Sciences Center (CCSA) in Universidade Federal do Rio Grande do Norte (UFRN).

Licensed by GPL 3.

## Setting up development environment
### ... for Linux (Debian based) users.

Make sure to use Python 3.5 and has its pip with virtualenv installed. Caution: at most Linux distributions,
the command ```python``` stands for python2 binary by default, and the same happens with ```pip```. 
If you're a Linux user, type ```python --version``` and ```pip --version``` to check if Python is
3.5 and its Pip is a 3.5 library. I'll give you a second tip: if there's
already a Python installed by default in your system, do not
try to change its standard version, it will probably confuse your system -- eg., my Ubuntu has Python
2 by default (```python --version``` outputs 2.7), so I installed Python 3 here for development purposes,
but I would never try to change my default ```python``` to 3.5 version, because my system needs its
standard Python interpreter typed just like that, so I have installed my Python 3 as ```python3```.
Once I activate my Virtual Environment (see the workflow below), I can check both my ```pip```and
```python``` versions, and they're now isolated from my operational system and are currently standing
for 3.5 (run the commands again and read the output to be sure). A third tip: having virtualenv
installed by pip from Python2 library doesn't mean you have virtualenv installed by pip3 from Python3 too.

You also need to make sure that an updated MongoDB is installed as well. The default Mongo from Debian
repository couldn't make it, so I installed following this tutorial:
<https://www.digitalocean.com/community/tutorials/como-instalar-o-mongodb-no-ubuntu-16-04-pt>. But just saying,
when I run ```mongo --version``` after starting mongo service, it outputs 3.2.12.

Now start by cloning this repository in a local folder and change directory to it.

```sh
$ git clone https://github.com/Mazuh/Minerva.git
$ cd Minerva/
```

Now, let's set up our temporary security file. Open ```./MinervaEnv/Minerva/fake/api_keys.json``` using your 
favorite text/code editor, copy its content without comments (by the way, read them) 
and paste at ```./MinervaEnv/Minerva/env/api_keys.json```
(this directory and this file will probably not exist, so create them before pasting anything, of course).
A suggestion that may work (note that I use ```nano``` editor, but it's a personal option):

```sh
$ mkdir ./MinervaEnv/Minerva/env/
$ touch ./MinervaEnv/Minerva/env/api_keys.json
$ cat ./MinervaEnv/Minerva/fake/api_keys.json > ./MinervaEnv/Minerva/env/api_keys.json
$ nano ./MinervaEnv/Minerva/env/api_keys.json 
# at editing its content, remove ALL COMMENT LINES from this new env/api_keys.json file
```

Use these command lines to create and activate the virtual environment:

```sh
$ cd ./MinervaEnv/
$ python3 -m virtualenv ./
$ source ./bin/activate
```

You will notice a ```(Minerva)``` prefixing your prompt string if it worked.
Now install all required libs:

```sh
$ pip install -r ./requirements.txt
```

After that, let's start a mongo service. Here, in my poor Ubuntu, I run:

```sh
$ sudo systemctl start mongod
$ sudo systemctl status mongod
```

And then I see, while running status operation, an output "Active: active (running)".

Assuming that there's no Minerva database installed, it's necessary to run a initial script
(only once, and never again). Consists of redirecting the content from ```i.js``` to ```mongo``` input.
There's a simple script for doing this (in case of something goes wrong, open the shell script and read 
it to learn what needs to be done, after check if there's an updated mongo service running):

```sh
$ cd ../dev_db/
$ chmod +x ./setup.sh
$ ./setup.sh --install
$ cd ../MinervaEnv
```

If packages installation went successfully and our configuration files are ok, you can
now start running the local server:

```sh
$ python runserver.py
```

Assuming that you did everything right, your terminal will output the URL for you to access using a web browser.
It should be http://localhost:4444/ but always read the output ("0.0.0.0" means it's opened for public access
and you need to know your IP address for using it instead of "localhost").

You should see the application running locally now. Any doubts, just open an issue here on GitHub!
