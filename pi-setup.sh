#!/usr/bin/env bash

sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt install python3.10
sudo apt install python3.10-venv

python3 -m venv ~/ads1115

cd ~/ads1115
source bin/activate

pip install -r requirements.txt