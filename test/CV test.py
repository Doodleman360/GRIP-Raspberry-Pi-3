#!/usr/bin/python3

"""
tests networktables from raspberry pi
"""

import cv2
import time


def main():
    print('Creating video capture')
    cap = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()




if __name__ == '__main__':
    main()
