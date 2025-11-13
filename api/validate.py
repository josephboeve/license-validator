from http.server import BaseHTTPRequestHandler
import json
import os

# Vercel KV for DB (free tier: 30k commands/month)
# Install: pip install redis (for KV)
# In Vercel dashboard, add KV store and get URL/TOKEN

import redis

kv = redis.from_url(os.environ.get('KV_URL'))  # Set in Vercel env vars

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        license_key = data.get('license_key')
        
        if not license_key:
            response = {'status': 'invalid'}
        else:
            status = kv.get(license_key)
            if status == b'active':
                response = {'status': 'valid'}
            else:
                response = {'status': 'invalid'}
        
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        return  # Disable logs
