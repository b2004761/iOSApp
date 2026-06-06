from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import socket


class ProfileHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        if path.endswith(".mobileconfig"):
            return "application/x-apple-aspen-config"
        if path.endswith(".webmanifest"):
            return "application/manifest+json"
        return super().guess_type(path)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


if __name__ == "__main__":
    port = 8765
    root = Path(__file__).resolve().parent
    import os

    os.chdir(root)
    server = ThreadingHTTPServer(("0.0.0.0", port), ProfileHandler)
    ip = local_ip()
    print(f"Open on this PC: http://127.0.0.1:{port}/")
    print(f"Open on iPhone:  http://{ip}:{port}/")
    print("Keep this window running while installing the profile.")
    server.serve_forever()
