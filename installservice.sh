#!/bin/bash

source include.sh

cp unit.service /tmp/unit.service

#replace things in unit file
sed -i -e "s/__workingdir__/${PWD}/g" /tmp/unit.service
sed -i -e "s/__servicedescription__/${servicedescription}/g" /tmp/unit.service

sudo cp /tmp/unit.service /etc/systemd/system/${servicename}.service
rm /tmp/unit.service
