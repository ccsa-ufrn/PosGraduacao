# Minerva

## About
Utility system for the workers and students of the 
postgraduate programs at Applied Social Sciences Center 
(CCSA) in Universidade Federal do 
Rio Grande do Norte (UFRN).

Licensed by GPL 3.

## Setting up development environment

Make sure to use Python 3.5 and has its pip with virtualenv installed. Caution: at most Linux distributions, the 
command python stands for python2 binary by default, and the same happens with pip. If're a Linux user, type
```python --version``` and ```pip --version``` to check the if Python is 3.5 and its Pip is a 3.5 library.
If you're a Windows or Mac user, then Google it (sorry about that). I'll give you a second tip: if
there's already a Python installed by default in your system, do not try to change its standard version, it will
probably confuse your system -- eg., my Ubuntu has Python 2 by default (```python --version``` outputs 2.7), so 
I installed Python 3 here for development purposes, but I would never try to change my default ```python``` to
3.5 version, because my system needs its standard Python interpreter typed just like that, so I have installed my
Python 3 as ```python3```. Once I activate my Virtual Environment (see the workflow below), I can check
both my ```pip```and ```python``` versions, and they're now isolated from my operational system and are currently
standing for 3.5 (run the commands again and read the output to be sure). A third tip: having virtualenv
installed by pip from Python2 library doesn't mean you have virtualenv installed by pip3 from Python3 too.

Start by cloning this repository in a local folder and change directory to it.

Then, already inside our repository root, use these command lines to create and activate the virtual environment:

```sh
$ cd ./MinervaEnv
$ python3 -m virtualenv ./
$ source ./bin/activate
```

(Quick tip: if you're using a Windows system, instead of ```./bin/activate``` then look for
```Scripts\activate.bat``` that doesn't even need ```python``` to run since '.bat' is a regular Win script)

You will notice a ```(Minerva)``` prefixing your prompt string if it worked.
Now install all required libs:

```sh
$ pip install -r ./requirements.txt
```

Now, let's set up our temporary security file. Open ```./fake/api_keys.json``` using your favorite text/code
editor, copy its content without comments (by the way, read them) and paste at ```./env/api_keys.json```
(this directory and this file may not exist, so create them before pasting anything, of course).

If packages installation went successfully and our configuration files are ok, you can
now start running the local server:

```sh
$ python runserver.py
```

Assuming that you did everything right, your terminal will output the URL for you to access using a web browser.
It should be http://localhost:4444/ but always read the output ("0.0.0.0" means it's opened for public access
and you need to know your IP address for using it instead of "localhost").

You should see the application running locally now. Any doubts, just open an issue here on GitHub!
