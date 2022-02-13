#!/bin/bash
#authbind would be necessary if the application binds to port 80 without root rights on linux
source .venv/bin/activate
#TODO: i know having this process in sudo is risky, but i have some functionality that needs sudo rights and it dont have time to make a clean solution for now
sudo python3.8 -m main
deactivate
