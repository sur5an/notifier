from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


def start_server():
    httpd = HTTPServer(('localhost', 1888), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    start_server()