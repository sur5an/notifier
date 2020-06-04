from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from document_db import Documents
import json
from cgi import parse_header, parse_multipart
import logging


def configure_logging():
    my_log_file_name = "db/" + os.path.basename(__file__) + ".log"
    logging.basicConfig(filename=my_log_file_name,
                        filemode='a',
                        format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                        datefmt='%D %H:%M:%S',
                        level=logging.INFO)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s,%(msecs)03d  %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/all":
            self.write_json(Documents().select_all())
            return
        if parsed_path.path == "/" or str(parsed_path.path).endswith("html")\
                or str(parsed_path.path).endswith(".js"):
            self.default()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path != "/addDoc" and parsed_path.path != "/deleteDoc":
            self.write_response("failed")
            return
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            post_vars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded' or ctype == "application/json":
            length = int(self.headers['content-length'])
            post_vars = json.loads(self.rfile.read(length))
        else:
            self.write_response("failed")
            return
        if parsed_path.path == "/addDoc":
            Documents().insert(post_vars)
        elif parsed_path.path == "/deleteDoc":
            Documents().delete(post_vars["id"])

        self.write_response("ok")

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
    configure_logging()
    httpd = HTTPServer(('0.0.0.0', 1888), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    start_server()
