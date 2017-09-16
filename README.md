# Plataforma de Pós-Graduação

## Version 1: Minerva

Utility system for the workers and students of the postgraduate programs at Applied Social 
Sciences Center (CCSA) in Universidade Federal do Rio Grande do Norte (UFRN).

This first goal is to start assembling data and providing basic information management.

License: [GPL 3](./LICENSE).

## Setting up development environment

This will show up how to start the project using Linux **Lubuntu 17.04** with virtualenv.

> Read [wiki](https://github.com/ccsa-ufrn/PosGraduacao/wiki/) for information about dockerized setup.

Having already installed:
  - Python 3.5 interpreter, ```python3``` (was already installed by default);
  - PyPI 9 client, ```pip3``` from 'python3-pip' package (usual ```sudo apt install``` command);
  - VirtualEnv module, ```python3 -m virtualenv``` command (usual ```sudo pip3 install``` script); and
  - MongoDB 3.2 and its shell ```mongo``` from an updated source (following [this Digital Ocean tutorial](https://www.digitalocean.com/community/tutorials/como-instalar-o-mongodb-no-ubuntu-16-04-pt)).

Now start by cloning this repository in a local folder and **c**hange **d**irectory to it.

### Virtualenv

Use these command lines to create and activate the virtual environment:

```sh
python3 -m virtualenv ./pgccsa_env/
source ./pgccsa_env/bin/activate
```

You will notice a ```(pgccsa_env)``` prefixing your prompt string if it worked.
Now install all required libs:

```sh
pip install -r ./requirements.txt
```

### API Keys

Open ```./settings/api_keys.json``` using your 
favorite text/code editor, copy its content without comments (by the way, read them) 
and paste at ```./settings/api_keys.fake.json```.
A suggestion that may work (note that I use ```nano``` editor, but it's a random option):

```sh
# copy the template content
cat ./settings/api_keys.fake.json > ./settings/api_keys.json 

# put valid authorization data while editing the real json
nano ./settings/api_keys.json
```

### Database server

Let's start a mongo service. Here I run:

```sh
sudo systemctl start mongod
sudo systemctl status mongod
```

We should see, after the last command line, an output "Active: active (running)".

Assuming that there's no Minerva database installed, it's necessary to run a initial script for inputting
some initial data. It consists of redirecting some scripts to ```mongo```:

```sh
mongo < ./settings/standard_installation.js
```

Please, check if mongo output looking for errors before proceding, everything should have been
well acknowledged. Make sure to have an updated Mongo service running too.

### Web server

If packages installation went successfully and our configuration files are ok, you can
now start running the local server:

```sh
python ./app.py
```

Assuming that you did everything right, your terminal will output the URL for you to
access using a web browser.
It should be http://localhost:4444/ but always read the output ("0.0.0.0:80" means you have super user
permission and your server it's opened for public access, so you need to know your IP address instead of "localhost" or "0.0.0.0").

You should see the application running now. Any doubts, just open an issue here on GitHub!
