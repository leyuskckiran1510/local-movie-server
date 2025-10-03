import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from player import Player
from tmdb import Search

searcher = Search()
player = Player()


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path.startswith('/static/'):
            filepath = path.lstrip('/')
            if os.path.exists(filepath):
                self.send_response(200)
                if filepath.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif filepath.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                else:
                    self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
            return

        if 'json' in params and 'query' in params:
            query = params['query'][0]
            results = searcher.search({'query': query})
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode('utf-8'))
            return

        if 'play' in params:
            tmdb_id = int(params['play'][0])
            ses = params.get('ses', [None])[0]
            ep = params.get('ep', [None])[0]
            embed_url = player.embed_url(tmdb_id, ses=ses, ep=ep)
            self.send_response(302)
            self.send_header('Location', embed_url)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('template.html', 'rb') as f:
            self.wfile.write(f.read())


def run(port: int = 8000):
    server = HTTPServer(('', port), MyHandler)
    print(f'Server running at http://127.0.0.1:{port}')
    server.serve_forever()


if __name__ == '__main__':
    run()
