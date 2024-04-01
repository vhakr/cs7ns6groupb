#!/bin/bash

docker network rm cafe-app-network 2>/dev/null
docker network create --subnet=172.16.0.0/12 --gateway=172.16.0.1 cafe-app-network

docker rm cafe-app-neimhin
docker run -d -it \
  --network cafe-app-nework \
  --name cafe-app-neimhin \
  --ip 172.17.0.0 \
  --add-host  neimhin:172.17.0.0 \
  --add-host  cian:172.17.0.1 \
  cafe-app-neimhin

docker rm cafe-app-cian
docker run -d -it \
  --network cafe-app-network \
  --name cafe-app-cian \
  --ip 172.17.0.1 \
  --add-host  neimhin:172.17.0.0 \
  --add-host  cian:172.17.0.1 \
  cafe-app-cian
