#!/bin/bash

while :
do
  DATE=$(date +"%Y-%m-%d_%H%M%S")
  raspistill -n -q 100 -t 100 -o /home/pi/camera/$DATE.jpg
  sleep 30
done