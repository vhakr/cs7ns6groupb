#!/bin/bash
docker build -t cafe-app-base       -f base.dockerfile .
docker build -t cafe-app-neimhin    -f neimhin.dockerfile .
docker build -t cafe-app-worker			-f worker.dockerfile .
docker build -t cafe-app-neimhin2   -f neimhin2.dockerfile .
docker build -t cafe-app-web-server -f web-server.dockerfile .
