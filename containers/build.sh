#!/bin/bash
docker build -t neimhin/cafe-app:base	  -f base.dockerfile .
docker build -t neimhin/cafe-app:neimhin  -f neimhin.dockerfile .
docker build -t neimhin/cafe-app:worker	  -f worker.dockerfile .
docker build -t neimhin/cafe-app:neimhin2 -f neimhin2.dockerfile .
docker build -t neimhin/cafe-app:cian	  -f cian.dockerfile .
