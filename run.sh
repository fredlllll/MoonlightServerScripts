#!/bin/bash
#authbind would be necessary if the application binds to port 80 without root rights on linux
source .venv/bin/activate
python3.10 -m main
deactivate
