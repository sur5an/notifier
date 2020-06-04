from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from document_db import Documents
import json


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/all":
            self.write_json(Documents().select_all())
            return

        self.default()

    def write_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode(encoding='utf_8'))

    def write_response(self, lines):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(lines, 'utf-8'))

    def default(self):
        f = open('index.html')
        lines = f.read()
        f.close()
        self.write_response(lines)


def start_server():
    httpd = HTTPServer(('0.0.0.0', 1888), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    start_server()