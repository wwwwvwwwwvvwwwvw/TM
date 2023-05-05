import http.server
import socketserver
import threading
import os
from urllib.parse import parse_qs

# The authentication function
def authenticate(username, password):
    with open("users.txt", "r") as users_file:
        for line in users_file:
            user, pwd = line.strip().split(':')
            if user == username and pwd == password:
                return True
    return False

# Custom request handler
class TestManagerRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(post_data)

        if self.path == "/login":
            username = data['username'][0]
            password = data['password'][0]

            if authenticate(username, password):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("test.html", "r") as test_file:
                    self.wfile.write(test_file.read().encode('utf-8'))
            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Invalid username or password")
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.path = "/login.html"

        return super().do_GET()

# The main function
def main():
    PORT = 8000

    Handler = TestManagerRequestHandler
    httpd = socketserver.ThreadingTCPServer(("", PORT), Handler)
    print("Test Manager is serving at port", PORT)

    httpd.serve_forever()

if __name__ == "__main__":
    main()
