#!/usr/bin/python3

"""
Detects stronghold goals using a usb camera plugged into raspberry pi
"""

import cv2
import networktables
from networktables import NetworkTable
from usb_GRIP import GripPipeline
import os
import sys
import logging
import time


def extra_processing(pipeline):
    """
    Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
    :param pipeline: the pipeline that just processed an image
    :return: None
    """
    center_x_positions = []
    center_y_positions = []
    widths = []
    heights = []

    # Find the bounding boxes of the contours to get x, y, width, and height
    for contour in pipeline.filter_contours_output:
        x, y, w, h = cv2.boundingRect(contour)
        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        widths.append(w)
        heights.append(y)
    # Publish to the '/vision' network table
    table = NetworkTable.getTable("/vision")
    table.putValue("centerX", NumberArray.from_list(center_x_positions))
    table.putValue("centerY", NumberArray.from_list(center_y_positions))
    table.putValue("width", NumberArray.from_list(widths))
    table.putValue("height", NumberArray.from_list(heights))


def main():
    logging.basicConfig(level=logging.DEBUG)
    print('Initializing NetworkTables')
    NetworkTable.setClientMode()
    NetworkTable.setIPAddress('10.11.57.2')
    NetworkTable.initialize()
    time.sleep(5)

    ready = False
    # maybe works?
    smartTable = NetworkTable
    while (not ready):
        try:
            smartTable = NetworkTable.getTable("/SmartDashboard")
            while (not smartTable.getValue("KeepAlive")):
                time.sleep(1)
            ready = True
        except KeyError as e:
            # print("Not ready!", end="", flush=True)
            ready = False
    
    print('Creating video capture')
    cap = cv2.VideoCapture(0)
    cap.set(15, smartTable.getValue("exposure"))

    print('Creating pipeline')
    pipeline = GripPipeline()

    print('Running pipeline')
    while 1:
        if (not smartTable.getValue("KeepAlive")):
            os.system('sudo shutdown -h now')
        have_frame, frame = cap.read()
        if have_frame:
            pipeline.process(frame)
            extra_processing(pipeline)

    print('Capture closed')


if __name__ == '__main__':
    main()
