#!/bin/bash

python3.8 -m venv ./.venv
source ./.venv/bin/activate
python3 -m pip install wheel
python3 -m pip install -r requirements.txt
deactivate