import json
## for python 2:
#from urlparse import urlparse, parse_qs
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
## for python 3:
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

DATA = {'message_to_send': 0}

def build_handler():
    class LayerDataHandler(BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            qs = parse_qs(urlparse(self.path).query)
            if 'message' in qs and len(qs['message']):
                #DATA['message_to_send'] = int(qs['message'][0])
                DATA['message_to_send'] = str(qs['message'][0])
            self.wfile.write(json.dumps(DATA['message_to_send']).encode('utf8'))

    return LayerDataHandler

if __name__ == '__main__':
    httpd = HTTPServer(('0.0.0.0', 5000), build_handler())
    print ('Server configured on port 5000')
    print ('Starting http server, use <Ctrl-C> to stop...')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    print ('Exiting...')
