#!/bin/bash
docker build -t cafe-app-base -f base.dockerfile .
docker build -t cafe-app-main -f main-region.dockerfile .
