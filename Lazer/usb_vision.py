#!/usr/bin/python3

"""
Detects lazer using a usb camera plugged into raspberry pi
"""

import cv2
import networktables
from networktables import NetworkTable
from griplazer import GripPipeline
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
    center_x = []
    center_y = []
    widths = []
    heights = []

    # Find the bounding boxes of the contours to get x, y, width, and height
    for contour in pipeline.filter_contours_output:
        x, y, w, h = cv2.boundingRect(contour)
        if (2 < (h/w)) & ((h/w) < 3):
            center_x.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
            center_y.append(y + h / 2)
            widths.append(w)
            heights.append(y)
    table = NetworkTable.getTable("/vision")
    if len(pipeline.filter_contours_output) > 1:
        # Publish to the '/vision' network table
        pti = (widths[0] / 5 + heights[0] / 2) / 2
        table.putValue("pti", pti)
        table.putValue("width", pipeline.resize_image_width)
        table.putValue("height", pipeline.resize_image_height)
        table.putValue("r1cX", center_x[0])
        table.putValue("r1cY", center_y[0])
        table.putValue("r1w", widths[0]/pti)
        table.putValue("r1h", heights[0]/pti)
        table.putValue("locked", True)
    else:
        table.putValue("locked", False)


def main():
    logging.basicConfig(level=logging.DEBUG)
    print('Initializing NetworkTables')
    NetworkTable.setClientMode()
    NetworkTable.setIPAddress('10.11.57.2')
    NetworkTable.initialize()
    time.sleep(1)

    ready = False
    # maybe works?
    smartTable = NetworkTable
    while not ready:
        try:
            smartTable = NetworkTable.getTable("/SmartDashboard")
            while not smartTable.getValue("KeepAlive"):
                time.sleep(1)
            ready = True
        except KeyError as e:
            # print("Waiting for connection!")
            ready = False

    print('Creating video capture')
    cap = cv2.VideoCapture(0)

    print('Creating pipeline')
    pipeline = GripPipeline()

    print('Running pipeline')
    while 1:
        if not smartTable.getValue("KeepAlive"):
            cap.release()
            cv2.destroyAllWindows()
            os.system('sudo shutdown -h now')
        have_frame, frame = cap.read()
        if have_frame:
            pipeline.process(frame)
            extra_processing(pipeline)
            ret, frame = cap.read()
            for contour in pipeline.filter_contours_output:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    print('Capture closed')


if __name__ == '__main__':
    main()
