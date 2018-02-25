#!/bin/bash

while :
do
  DATE=$(date +"%Y-%m-%d_%H%M")
  raspistill -t 900000 -tl 30000 -o /home/pi/camera/$DATE%d.jpg
done