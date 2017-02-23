from PIL import Image
import threading
import http.server
from socketserver import ThreadingMixIn
from io import StringIO
import cv2
from grip import GripPipeline
import logging
import time
import threading
cap = None

class AnotherHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(client):
        client.send_response(200)
        client.send_header("Content-type", "text/html")
        client.end_headers()
    def do_GET(client):
        ret, frame = cap.read()
        pipeline.process(frame)
        for contour in pipeline.filter_contours_output:
            x, y, w, h = cv2.boundingRect(contour)
            if (2 < (h / w)) & ((h / w) < 3):
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(imgRGB)
        jpg.save("/home/pi/GRIP-Raspberry-Pi-3/USB/WEB/IMG.mjpg", 'JPEG')
        if client.path == "/":
            client.send_response(200)
            client.send_header("Content-type", "image/jpg")
            client.end_headers()

            client.wfile.write(load_binary('/home/pi/GRIP-Raspberry-Pi-3/USB/WEB/IMG.mjpg'))

def load(file):
    with open(file, 'r') as file:
        return encode(str(file.read()))

def encode(file):
    return bytes(file, 'UTF-8')

def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print(self.wfile)
        self.wfile.write(bytes('<img src="http://127.0.0.1:8080/WEB/IMG.mjpg"/>', "UTF-8"))
        self.wfile.write(bytes("<body><p>This is a test.</p>", "UTF-8"))
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "UTF-8"))
        self.wfile.write(bytes("</body></html>", "UTF-8"))

class CamHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("Refresh")
        print(threading.currentThread().getName())
        print(self.path)
        if self.path.endswith('.html'):
            self.send_responseself.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bites('<html><head></head><body>', "UTF-8"))
            self.wfile.write('<img src="http://10.11.57.10:8080/WEB/IMG.mjpg"/>')
            self.wfile.write('</body></html>')
            return    
        """else:
            self.send_response(200)
            self.end_headers()
            message =  threading.currentThread().getName()
            self.wfile.write(message)
            self.wfile.write('\n')
            return"""
        #if self.path.endswith('.mjpg'):
        """if True:
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            if True:    
                print("running")
                try:
                    rc, frame = cap.read()
                    pipeline.process(frame)
                    for contour in pipeline.filter_contours_output:
                        x, y, w, h = cv2.boundingRect(contour)
                        if (2 < (h / w)) & ((h / w) < 3):
                            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    cv2.imshow('frame', frame)
                    cv2.waitKey(1)
                    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    jpg = Image.fromarray(imgRGB)
                    jpg.save("/home/pi/GRIP-Raspberry-Pi-3/USB/WEB/IMG.jpeg", 'JPEG')
                    jpg.save(self.wfile, 'JPEG')
                    #time.sleep(0.05)
                except KeyboardInterrupt:
        if True:
            self.send_response(200)
            self.end_headers()
            self.wfile.write('<img src="http://127.0.0.1:8080/WEB/IMG.jpeg"/>')
            return
        """
        
class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
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
    server = None
    try:
        server = ThreadedHTTPServer(('localhost', 8080), AnotherHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        cap.release()
        server.socket.close()
    while 1:
        ret, frame = cap.read()
        pipeline.process(frame)
        for contour in pipeline.filter_contours_output:
            x, y, w, h = cv2.boundingRect(contour)
            if (2 < (h / w)) & ((h / w) < 3):
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(imgRGB)
        jpg.save("/home/pi/GRIP-Raspberry-Pi-3/USB/WEB/IMG.mjpg", 'JPEG')
        #jpg.save(self.wfile, 'JPEG')

if __name__ == '__main__':
    main()
