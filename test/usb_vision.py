#!/usr/bin/python3

"""
tests networktables from raspberry pi
"""

import networktables
from networktables import NetworkTable
import os
import sys
import logging
import time


def main():
    logging.basicConfig(level=logging.DEBUG)
    print('Initializing NetworkTables')
    NetworkTable.setClientMode()
    #NetworkTable.setIPAddress()
    NetworkTable.initialize(server=sys.argv[1])
    time.sleep(10)
    try:
        table = NetworkTable.getTable("/SmartDashboard")
        #table.putValue("centerX", 2)
        table.putValue("centerY", 3)
        table.putValue("width", 4)
        table.putValue("height", 5)
        print(table.getValue("centerX"));

    except KeyError as e:
        print(e)
    smartTable = NetworkTable.getTable("/SmartDashboard")
    while 1:
        if (not smartTable.getValue("KeepAlive")):
            os.system('shutdown now -h')
        



if __name__ == '__main__':
    main()
