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
            if (2 < (h / w)) and ((h / w) < 3):
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        #TODO: compress image
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(imgRGB)
        jpg.save("/home/pi/GRIP-Raspberry-Pi-3/USB/WEB/IMG.mjpg", 'JPEG')
        if client.path == "/":
            client.send_response(200)
            client.send_header("Content-type", "text/html")
            client.end_headers()
            client.wfile.write(load('/home/pi/GRIP-Raspberry-Pi-3/USB/WEB/index.html'))
      
        if client.path[:4] == "/IMG":
            client.send_response(200)
            client.send_header("Content-type", "image/jpg")
            client.end_headers()
            try: 
                client.wfile.write(load_binary('/home/pi/GRIP-Raspberry-Pi-3/USB/WEB/IMG.mjpg'))
            except BrokenPipeError as e:
                if False:
                    print(e)
                if False:
                    print("table flip")
            
def load(file):

    with open(file, 'r') as file:
        return encode(str(file.read()))

def encode(file):
    return bytes(file, 'UTF-8')

def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()
        
class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""

def main():
    log = logging.getLogger('werkkzeug')
    log.setLevel(logging.ERROR)
    
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
        server = ThreadedHTTPServer(('0.0.0.0', 8080), AnotherHandler)
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
            if (2 < (h / w)) and ((h / w) < 3):
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(imgRGB)
        jpg.save("/home/pi/GRIP-Raspberry-Pi-3/USB/WEB/IMG.mjpg", 'JPEG')
        #jpg.save(self.wfile, 'JPEG')

if __name__ == '__main__':
    main()