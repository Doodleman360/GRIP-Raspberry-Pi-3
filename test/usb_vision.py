#!/usr/bin/python3

"""
tests networktables from raspberry pi
"""

import networktables
from networktables import NetworkTable
import os
import sys
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    print('Initializing NetworkTables')
    NetworkTable.setClientMode()
    #NetworkTable.setIPAddress()
    NetworkTable.initialize(server=sys.argv[1])
    
    table = NetworkTable.getTable("vision")
    #table.putValue("centerX", 2)
    table.putValue("centerY", 3)
    table.putValue("width", 4)
    table.putValue("height", 5)
    print(table.getValue("asdf"));
    #os.system('shutdown now -h')



if __name__ == '__main__':
    main()
