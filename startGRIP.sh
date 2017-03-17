#!/bin/sh
sudo v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_absolute=5
lxterminal -e python3 /home/pi/GRIP-Raspberry-Pi-3/USB/WEB/webserver.py
sudo python3 /home/pi/GRIP-Raspberry-Pi-3/USB/usb_vision.py 
