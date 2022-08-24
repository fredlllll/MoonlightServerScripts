#!/bin/bash

set -o errexit

sudo apt install python3.10-venv
python3.10 -m venv ./.venv
source ./.venv/bin/activate
python3 -m pip install wheel
python3 -m pip install -r requirements.txt
deactivate