[![PyPI](https://img.shields.io/pypi/v/adminbot.svg)](https://pypi.python.org/pypi/adminbot)
[![license MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/Dih5/adminbot/master/LICENSE.txt)


# adminbot
A python-implemented telegram bot to admin your server.


* [Features](#features)
* [Overview](#overview)
* [Installation](#installation)
* [Running](#running)

## Overview
![alt tag](https://raw.github.com/dih5/adminbot/master/img/1.png)
![alt tag](https://raw.github.com/dih5/adminbot/master/img/2.png)
![alt tag](https://raw.github.com/dih5/adminbot/master/img/3.png)

## Features
The package deploys a telegram bot with the following capabilities:
* Remote python interpreter.
* Send matplotlib images. Yeah, plot a sine or two a send them to your mobile. You'll be the soul of the party.
* Run shell commands.
* Use-related commands (disk use, check cpu-consuming processes).


## Installation
Assuming you have [python](https://www.python.org/) with [pip](https://pip.pypa.io/en/stable/installing/):
* To install the last 'stable' version from pypi: ```pip install adminbot```. Do not expect much stability in the API though...
* To install the last development version: ```pip install https://github.com/dih5/adminbot/archive/master.zip```. 

## Running
If you are new to telegram bots first check the [official introduction](https://core.telegram.org/bots) and create a bot using the [BotFather](https://core.telegram.org/bots#6-botfather).
Create a file following [example.json]((https://raw.github.com/dih5/adminbot/master/example.json)), using your bot's token. For the bot to answer your commands you must add your user id to the adminlist. Don't worry if you don't know it yet.
Run the bot using ```adminbot example.json``` . If everything went right you should be able to talk to it in from your telegram client.

If you did not add your user id to the admin list you will see it in the console when the bot receives a message. Add it and restart the bot.

