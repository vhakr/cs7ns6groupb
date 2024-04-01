#!/bin/bash
docker build --progress=plain -t cafe-app-base    -f base.dockerfile .
docker build --progress=plain -t cafe-app-neimhin -f neimhin.dockerfile .
docker build --progress=plain -t cafe-app-cian    -f cian.dockerfile .
