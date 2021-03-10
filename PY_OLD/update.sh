#!/bin/bash

source include.sh

sudo systemctl stop ${servicename}
git pull
sudo systemctl start ${servicename}
