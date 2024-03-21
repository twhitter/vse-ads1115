#!/usr/bin/env bash

sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt install python3.10
sudo apt install python3.10-venv

#python3 -m venv ads1115
source ads1115/bin/activate

#pip3 install -r requirements.txt

python3 test.py