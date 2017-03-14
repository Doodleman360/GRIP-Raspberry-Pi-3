import threading
import http.server
from socketserver import ThreadingMixIn
from io import StringIO
import logging
import time
import threading

class AnotherHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(client):
        client.send_response(200)
        client.send_header("Content-type", "text/html")
        client.end_headers()
    def do_GET(client):
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
    server = None
    try:
        server = ThreadedHTTPServer(('0.0.0.0', 8080), AnotherHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        cap.release()
        server.socket.close()

if __name__ == '__main__':
    main()
