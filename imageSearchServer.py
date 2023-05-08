from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
from imageSearch import *
import json
port = 8080
class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            params = urllib.parse.parse_qs(self.path[2:])
            page = int(params["page"][0])
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)
            urls, count, numResultsPerPage, time = imageSearch(body, page)
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps({"urls":urls, "count":count, "numResultsPerPage":numResultsPerPage, "time":time}).encode("utf-8"))
        except:
            self.send_response(400)
            self.end_headers()

httpd = HTTPServer(('localhost', port), RequestHandler)
print("Image Search Server listening on port " + str(port))
httpd.serve_forever()