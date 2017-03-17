#!/usr/bin/python3

"""
"""

import cv2
import networktables
from networktables import NetworkTable
from grip import GripPipeline
import os
import sys
import logging
import time
import random

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
        if (2 < (h/w)) and ((h/w) < 3):
            center_x.append(x + w / 2)
            center_y.append(y + h / 2)
            widths.append(w)
            heights.append(y)
    table = NetworkTable.getTable("/vision")
    table.putValue("PIrand", random.random())
    if len(widths) == 2:
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

def shutdown():
    #cap.release()
    #cv2.destroyAllWindows()
    #table.putValue("locked", False)
    #os.system('sudo shutdown -h now')
    os.system('echo shutdown should have hapeded by now')

def main():
    logging.basicConfig(level=logging.DEBUG)
    print('Initializing NetworkTables')
    NetworkTable.setClientMode()
    NetworkTable.setIPAddress('10.11.57.2')
    NetworkTable.initialize()
    time.sleep(1)

    ready = False
    smartTable = NetworkTable

    #Auto shutdown
    rndNumber = 0
    seconds = 0

    print("waiting for networktables")
    while not ready:
        try:
            smartTable = NetworkTable.getTable("/SmartDashboard")
            while not smartTable.getValue("KeepAlive"):
                time.sleep(1)
            ready = True
        except KeyError as e:
            # print("Waiting for connection!")
            ready = False
            
    print("conected to networktables")
    
    table = NetworkTable.getTable("/vision")
    
    print('Creating video capture')
    cap = cv2.VideoCapture(0)
    table.putValue("width", cap.get(3))
    table.putValue("height", cap.get(4))

    print('Creating pipeline')
    pipeline = GripPipeline()

    ##process = 0
    print("waiting for shutdown timer to start")
    rndNumber = smartTable.getValue("random")
    while rndNumber == smartTable.getValue("random"):
        time.sleep(0.1)
    print("main loop")
    while 1:
        if not smartTable.getValue("KeepAlive"):
            shutdown()

        ########
        if rndNumber != smartTable.getValue("random"):
            rndNumber = smartTable.getValue("random")
            seconds = int(round(time.time()))
        else:
            #print('shutting down in ' + (int(round(time.time())) - seconds))
            if int(round(time.time())) - seconds >= 10:
                shutdown()
        ########
                
        have_frame, frame = cap.read()
        if have_frame:
            pipeline.process(frame)
            extra_processing(pipeline)
            ret, frame = cap.read()
            
            if(len(pipeline.filter_contours_output) < 2):
                print("widen")
                pipeline.widen()
            if(len(pipeline.filter_contours_output) > 2):
                print("contract")
                pipeline.contract()
                
            for contour in pipeline.filter_contours_output:
                x, y, w, h = cv2.boundingRect(contour)
                if (2 < (h/w)) and ((h/w) < 3):
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv2.imshow('frame', frame)
            
            #TODO: compress image
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            jpg = Image.fromarray(imgRGB)
            jpg.save("/home/pi/GRIP-Raspberry-Pi-3/USB/WEB/IMG.mjpg", 'JPEG')
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                table.putValue("locked", False)
                break

    print('Capture closed')


if __name__ == '__main__':
    main()
