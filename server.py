import http.server, ssl, subprocess, os, sys

certfile = '/tmp/singularity-cert.pem'
keyfile = '/tmp/singularity-key.pem'

# Generate self-signed cert if missing
if not os.path.exists(certfile):
    subprocess.run([
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', keyfile, '-out', certfile,
        '-days', '365', '-nodes',
        '-subj', '/CN=localhost'
    ], check=True, capture_output=True)

port = 8443
handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(('', port), handler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile, keyfile)
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

print(f'HTTPS server running at https://localhost:{port}')
httpd.serve_forever()
