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

def main():
    logging.basicConfig(level=logging.DEBUG)
    
    print('Creating video capture')
    cap = cv2.VideoCapture(0)

    print('Creating pipeline')
    pipeline = GripPipeline()

    print('Running pipeline')
    while 1:
        have_frame, frame = cap.read()
        if have_frame:
            pipeline.process(frame)
            ret, frame = cap.read()
            for contour in pipeline.filter_contours_output:
                x, y, w, h = cv2.boundingRect(contour)
                if (2 < (h/w)) & ((h/w) < 3):
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    print('Capture closed')


if __name__ == '__main__':
    main()
