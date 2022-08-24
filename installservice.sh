#!/bin/bash

set -o errexit

source include.sh

cp unit.service /tmp/unit.service

#replace things in unit file
sed -i -e "s~__workingdir__~${PWD}~g" /tmp/unit.service
sed -i -e "s~__user__~${serviceuser}~g" /tmp/unit.service
sed -i -e "s~__group__~${servicegroup}~g" /tmp/unit.service
sed -i -e "s~__servicedescription__~${servicedescription}~g" /tmp/unit.service

sudo cp /tmp/unit.service /etc/systemd/system/${servicename}.service
rm /tmp/unit.service

sudo systemctl daemon-reload
