#!/bin/bash
docker build -t cafe-app-base       -f base.dockerfile .
docker build -t cafe-app-neimhin    -f neimhin.dockerfile .
docker build -t cafe-app-cian       -f cian.dockerfile .
docker build -t cafe-app-web-server -f web-server.dockerfile .
