#!/usr/bin/python3

"""
Detects stronghold goals using a usb camera plugged into raspberry pi
"""

#import cv2
import networktables
from networktables import NetworkTable
#from usb_GRIP import GripPipeline


def main():
    print('Initializing NetworkTables')
    NetworkTable.setClientMode()
    NetworkTable.setIPAddress('172.22.11.1')
    NetworkTable.initialize()
    
    table = NetworkTable.getTable("/vision")
    table.putValue("centerX", 2))
    table.putValue("centerY", 3))
    table.putValue("width", 4)
    table.putValue("height", 5)
    os.system('shutdown now -h')



if __name__ == '__main__':
    main()
