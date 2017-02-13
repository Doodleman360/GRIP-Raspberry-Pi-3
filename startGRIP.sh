#!/bin/sh
sudo v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_absolute=5

sudo python3 /home/pi/GRIP-Raspberry-Pi-3/USB/usb_vision.py > /home/pi/Desktop/log.txt
