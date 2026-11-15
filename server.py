"""
Lightweight HTTP Server for R Harshitha's Portfolio
Serves static portfolio files and handles contact form submissions.
"""
import os
import json
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

DEFAULT_PORT = 8000
HOST = "127.0.0.1"

# Set base dir to directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "contacts.json")

# Ensure data dir exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

class PortfolioHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS for local testing
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # API to view received contact messages
        if self.path in ("/api/contact", "/api/contacts"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    messages = json.load(f)
            except Exception:
                messages = []
            self.wfile.write(json.dumps({"success": True, "messages": messages}).encode("utf-8"))
            return
        
        # Default static file serving
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/contact":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length).decode("utf-8")
            
            try:
                data = json.loads(post_body)
            except json.JSONDecodeError:
                import urllib.parse
                parsed = urllib.parse.parse_qs(post_body)
                data = {k: v[0] for k, v in parsed.items()}
            
            # Format entry
            entry = {
                "name": data.get("name", "").strip(),
                "email": data.get("email", "").strip(),
                "subject": data.get("subject", "").strip(),
                "type": data.get("type", "General Inquiry"),
                "message": data.get("message", "").strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Save to JSON
            try:
                with open(DATA_FILE, "r+", encoding="utf-8") as f:
                    try:
                        records = json.load(f)
                    except Exception:
                        records = []
                    records.append(entry)
                    f.seek(0)
                    f.truncate()
                    json.dump(records, f, indent=2)
            except Exception as e:
                print(f"Error saving contact message: {e}")

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            response = {
                "success": True,
                "message": f"Thank you, {entry.get('name', 'there')}! Your message has been sent successfully. I will get back to you shortly."
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        self.send_error(404, "Not Found")

    def guess_type(self, path):
        # Ensure correct MIME type for PDF and modern assets
        if path.endswith(".pdf"):
            return "application/pdf"
        elif path.endswith(".svg"):
            return "image/svg+xml"
        elif path.endswith(".css"):
            return "text/css"
        elif path.endswith(".js"):
            return "application/javascript"
        return super().guess_type(path)

def run():
    port = DEFAULT_PORT
    for p in [DEFAULT_PORT, 8080, 8081, 5000]:
        try:
            server_address = (HOST, p)
            httpd = HTTPServer(server_address, PortfolioHandler)
            port = p
            break
        except OSError:
            continue

    print(f"======================================================")
    print(f"  R Harshitha's Portfolio Server is running!")
    print(f"  URL: http://localhost:{port} or http://{HOST}:{port}")
    print(f"  Serving files from: {BASE_DIR}")
    print(f"======================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == "__main__":
    run()
