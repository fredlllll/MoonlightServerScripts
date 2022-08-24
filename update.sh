#!/bin/bash

set -o errexit

source include.sh

sudo systemctl stop ${servicename}
git pull
sudo systemctl start ${servicename}
