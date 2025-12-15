#!/usr/bin/env python3
"""
ADB HTTP Bridge - Exposes ADB commands via HTTP for Goose Mobile
Run this on the computer connected to the emulator.
"""

import subprocess
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class ADBHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/screenshot":
            self.handle_screenshot()
        elif path == "/health":
            self.send_json({"status": "ok"})
        else:
            self.send_error(404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length else "{}"

        try:
            data = json.loads(body) if body else {}
        except:
            data = {}

        if path == "/click":
            x = data.get("x", 0)
            y = data.get("y", 0)
            self.handle_click(x, y)
        elif path == "/tap":
            x = data.get("x", 0)
            y = data.get("y", 0)
            self.handle_click(x, y)
        elif path == "/swipe":
            x1, y1 = data.get("x1", 0), data.get("y1", 0)
            x2, y2 = data.get("x2", 0), data.get("y2", 0)
            duration = data.get("duration", 300)
            self.handle_swipe(x1, y1, x2, y2, duration)
        elif path == "/input":
            text = data.get("text", "")
            self.handle_input(text)
        elif path == "/keyevent":
            keycode = data.get("keycode", "")
            self.handle_keyevent(keycode)
        elif path == "/shell":
            cmd = data.get("cmd", "")
            self.handle_shell(cmd)
        elif path == "/start_app":
            package = data.get("package", "")
            self.handle_start_app(package)
        else:
            self.send_error(404)

    def handle_screenshot(self):
        """Capture screenshot via ADB and return as base64"""
        try:
            result = subprocess.run(
                ["adb", "exec-out", "screencap", "-p"],
                capture_output=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout:
                b64 = base64.b64encode(result.stdout).decode('utf-8')
                self.send_json({
                    "success": True,
                    "image": f"data:image/png;base64,{b64}",
                    "size": len(result.stdout)
                })
            else:
                self.send_json({
                    "success": False,
                    "error": result.stderr.decode('utf-8') if result.stderr else "Unknown error"
                })
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})

    def handle_click(self, x, y):
        """Tap at coordinates"""
        try:
            result = subprocess.run(
                ["adb", "shell", "input", "tap", str(x), str(y)],
                capture_output=True,
                timeout=5
            )
            self.send_json({"success": True, "x": x, "y": y})
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})

    def handle_swipe(self, x1, y1, x2, y2, duration):
        """Swipe gesture"""
        try:
            result = subprocess.run(
                ["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)],
                capture_output=True,
                timeout=5
            )
            self.send_json({"success": True})
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})

    def handle_input(self, text):
        """Input text"""
        try:
            # Escape special characters
            escaped = text.replace(" ", "%s").replace("'", "\\'")
            result = subprocess.run(
                ["adb", "shell", "input", "text", escaped],
                capture_output=True,
                timeout=5
            )
            self.send_json({"success": True})
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})

    def handle_keyevent(self, keycode):
        """Send keyevent"""
        try:
            result = subprocess.run(
                ["adb", "shell", "input", "keyevent", str(keycode)],
                capture_output=True,
                timeout=5
            )
            self.send_json({"success": True})
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})

    def handle_shell(self, cmd):
        """Execute shell command"""
        try:
            result = subprocess.run(
                ["adb", "shell"] + cmd.split(),
                capture_output=True,
                timeout=10
            )
            self.send_json({
                "success": True,
                "stdout": result.stdout.decode('utf-8'),
                "stderr": result.stderr.decode('utf-8')
            })
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})

    def handle_start_app(self, package):
        """Start an app"""
        try:
            result = subprocess.run(
                ["adb", "shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"],
                capture_output=True,
                timeout=5
            )
            self.send_json({"success": True, "package": package})
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def log_message(self, format, *args):
        print(f"[ADB Bridge] {args[0]}")

def main():
    port = 8765
    server = HTTPServer(("0.0.0.0", port), ADBHandler)
    print(f"ADB HTTP Bridge running on http://0.0.0.0:{port}")
    print(f"Endpoints:")
    print(f"  GET  /screenshot     - Capture screen")
    print(f"  GET  /health         - Health check")
    print(f"  POST /click          - Tap at x,y")
    print(f"  POST /swipe          - Swipe gesture")
    print(f"  POST /input          - Input text")
    print(f"  POST /start_app      - Start app by package")
    print(f"  POST /shell          - Execute shell command")
    server.serve_forever()

if __name__ == "__main__":
    main()
