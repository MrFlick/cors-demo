from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

if __name__ == '__main__':
    path_cert = "certs/site.crt"
    path_key = "certs/site.key"
    server_host = '0.0.0.0'
    server_port = 8000
    httpd = HTTPServer((server_host, server_port), SimpleHTTPRequestHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        keyfile=path_key,
        certfile=path_cert)
    httpd.socket = context.wrap_socket(httpd.socket,
        server_side=True)

    print(f"Serving HTTPS on https://{server_host}:{server_port}")
    print(f"Ctrl-C to quit")
    httpd.serve_forever()