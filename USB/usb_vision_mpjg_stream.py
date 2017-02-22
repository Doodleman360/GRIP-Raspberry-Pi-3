import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import cv2
from grip import GripPipeline
import logging
import time
cap = None


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    rc, img = cap.read()
                    if not rc:
                        continue
                    pipeline.process(img)
                    # ret, frame = cap.read()
                    frame = None
                    for contour in pipeline.filter_contours_output:
                        x, y, w, h = cv2.boundingRect(contour)
                        if (2 < (h / w)) & ((h / w) < 3):
                            frame = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    cv2.imshow('frame', img)
                    #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    jpg = Image.fromarray(frame)
                    tmpFile = StringIO.StringIO()
                    jpg.save(tmpFile, 'JPEG')
                    self.wfile.write("--jpgboundary")
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(tmpFile.len))
                    self.end_headers()
                    jpg.save(self.wfile, 'JPEG')
                    time.sleep(0.05)
                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://127.0.0.1:8080/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    logging.basicConfig(level=logging.DEBUG)
    
    print('Creating video capture')
    global cap
    cap = cv2.VideoCapture(0)

    print('Creating pipeline')
    global pipeline
    pipeline = GripPipeline()

    print('Running pipeline')
    global img
    try:
        server = ThreadedHTTPServer(('localhost', 8080), CamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        cap.release()
        server.socket.close()

if __name__ == '__main__':
    main()
