#!/usr/bin/env bash

set -o errexit
set -o nounset

if [ ! -f mongorootpasswd ]
then
  echo "missing password file mongorootpasswd"
  exit;
fi

docker volume create local-mongo-data
docker run -d -p 27017:27017 --name local-mongo -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=$(cat mongorootpasswd) -v local-mongo-data:/data/db mongo
