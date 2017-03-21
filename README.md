# Minerva

## About
Utility system for the workers and students of the 
postgraduate programs at Applied Social Sciences Center 
(CCSA) in Universidade Federal do 
Rio Grande do Norte (UFRN).

Licensed by GPL 3.

## Setting up development environment

Make sure to use Python 3.5 and has its pip with virtualenv installed. Caution: at most Linux distributions, the command python stands for python2 binary by default, and the same happens with pip. So, below here, I type python3 and pip3 only because they're Lubuntu 16.10 default binaries for my desired versions; but these commands may be typed differently in your local machine, so just be aware of the versions that you're using here and everything should be ok (ie, if you type 'python' and your OS use python 3.5, then it's fine for you to keep typing 'python', and so on).

Start by cloning this repository in a local folder and change directory to it.

Then, already inside our repository root, use this command lines to create and activate the virtual environment:

```
$ cd ./MinervaEnv
$ python3 -m virtualenv ./
$ source ./bin/activate
```

(Quick tip: if you're using a Windows, instead of ```./bin/activate``` then look for ```./Scripts/activate.bat``` that doesn't even need 'python' to run since .bat is a regular Win script)

You will notice a ```(Minerva)``` prefixing your prompt string if it worked.
Now install all required libs:

```
$ pip3 install -r ./requirements.txt
```

If packages installation went successfully, you can now start the local server:

```
$ python3 runserver.py
```

If you did everything right, your terminal will output the URL for you to access using a web browser.
It should be http://localhost:4444/ but read the output to be sure.

You should see the application running locally now. And doubts, open an issue!
