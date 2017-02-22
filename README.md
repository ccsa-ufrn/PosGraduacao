# Minerva

## About
Utility system for the workers and students of the 
postgraduate programs at Applied Social Sciences Center 
(CCSA) in Universidade Federal do 
Rio Grande do Norte (UFRN).

Under GPL 3.

## Setting up development enviroment

Make sure to use Python 3.5.3 and has pip and virtualenv installed.
Start by cloning this repository in a local folder and change directory to it.

Already inside our (relative) root, use this command lines:

$ cd Minerva

Do not get confused: after using the command above, if you try executing "ls", you should see a file
named requirements.txt, and not readme.md, license nor other root repository files.

And now, at this Minerva homonic subfolder, create and activate a virtual environment.

$ virtualenv . 
$ ./Scripts/activate

You will notice a (Minerva) prefixing your prompt string if it worked.
And then install all required libs:

$ pip install -r ./requirements.txt

If packages installation went successfully, you can now start the local server.
Once again, change directory to another hominic subsubfolder called Minerva:

$ cd Minerva
$ python runserver.py

Caution, most Linux distributions use binary python as python2 by default, so pay attention
and use the required Python version at the beggining of this readme file.

If you did everything fine, your terminal will output the URL for you to access using a web browser.
By default, it's http://localhost:5555/ but read the output to be sure. 

You'll see then the application running locally.
