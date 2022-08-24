#!/bin/bash

set -o errexit

python3.10 -m venv ./.venv
source ./.venv/bin/activate
python3 -m pip install wheel
python3 -m pip install -r requirements.txt
deactivate