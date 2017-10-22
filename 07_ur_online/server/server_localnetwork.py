import json
import logging
## for python 2:
#from urlparse import urlparse, parse_qs
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
## for python 3:
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger()

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
            self.wfile.write(json.dumps(DATA['message_to_send'],
            ensure_ascii=False).encode('utf8'))

    return LayerDataHandler

if __name__ == '__main__':
    from sys import argv

    if len(argv) > 1:
        http_port = int(argv[1])
    else:
        http_port = 5000

    httpd = HTTPServer(('0.0.0.0', http_port), build_handler())
    LOG.info('Server configured on port %d, for a different port, start with: python server.py [http_port]', http_port)
    LOG.info('Starting http server, use <Ctrl-C> to stop...')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    LOG.info('Exiting...')
