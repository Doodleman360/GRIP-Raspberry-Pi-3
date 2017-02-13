#!/usr/bin/python3

"""
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
    :return: None
    """
    center_x = []
    center_y = []
    widths = []
    heights = []

    for contour in pipeline.filter_contours_output:
        x, y, w, h = cv2.boundingRect(contour)
        if (2 < (h/w)) & ((h/w) < 3):
            center_x.append(x + w / 2)
            center_y.append(y + h / 2)
            widths.append(w)
            heights.append(y)
    table = NetworkTable.getTable("/vision")
    if len(widths) > 1:
        # Publish to the '/vision' network table
        pti = (widths[0] / 5 + heights[0] / 2) / 2
        table.putValue("pti", pti)
        table.putValue("r1cX", center_x[0])
        table.putValue("r1cY", center_y[0])
        table.putValue("r1w", widths[0]/pti)
        table.putValue("r1h", heights[0]/pti)
        table.putValue("r2cX", center_x[1])
        table.putValue("r2cY", center_y[1])
        table.putValue("r2w", widths[1]/pti)
        table.putValue("r2h", heights[1]/pti)
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

    table = NetworkTable.getTable("/vision")
    
    print('Creating video capture')
    cap = cv2.VideoCapture(0)
    table.putValue("width", cap.get(3))
    table.putValue("height", cap.get(4))

    print('Creating pipeline')
    pipeline = GripPipeline()

    print('Running pipeline')
    while 1:
        if not smartTable.getValue("KeepAlive"):
            cap.release()
            cv2.destroyAllWindows()
            table.putValue("locked", False)
            os.system('sudo shutdown -h now')
        have_frame, frame = cap.read()
        if have_frame:
            pipeline.process(frame)
            extra_processing(pipeline)
            ret, frame = cap.read()
            for contour in pipeline.filter_contours_output:
                x, y, w, h = cv2.boundingRect(contour)
                if (2 < (h/w)) & ((h/w) < 3):
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                table.putValue("locked", False)
                break

    print('Capture closed')


if __name__ == '__main__':
    main()
