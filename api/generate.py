from http.server import BaseHTTPRequestHandler
import json
import secrets
import os
import redis

kv = redis.from_url(os.environ.get('KV_URL'))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        new_key = secrets.token_hex(16)
        kv.set(new_key, 'active')
        response = {'key': new_key}
        
        self.wfile.write(json.dumps(response).encode())
