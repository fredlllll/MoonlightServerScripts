#!/bin/bash
#authbind is necessary so the application can bind to port 80 without root rights on linux
source venv/bin/activate
#authbind --deep python3.8 -m main.py
#dont need authbind for moonlight cause we use other port
python3.8 -m main.py
deactivate