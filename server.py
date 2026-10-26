#!/usr/bin/env python3
"""
FlowGrid — Lightweight HTTP Backend & C++ Fenwick Tree Bridge
Data Structures & Algorithms (DSA) Case Study Project

Provides HTTP REST endpoints for the FlowGrid traffic analytics dashboard
and delegates all Fenwick Tree operations to the compiled C++ executable.
Zero external dependencies (uses Python standard library only).
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

# Base directories
BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"

# Locate C++ binary
EXE_NAME = "traffic_analytics.exe" if os.name == "nt" else "traffic_analytics"
BIN_CANDIDATES = [
    BASE_DIR / "bin" / EXE_NAME,
    BASE_DIR.parent / "bin" / EXE_NAME,
    BASE_DIR / EXE_NAME,
]

CPP_EXE = None
for cand in BIN_CANDIDATES:
    if cand.is_file():
        CPP_EXE = cand
        break

if CPP_EXE is None:
    CPP_EXE = BASE_DIR / "bin" / EXE_NAME

# Initial benchmark corridor traffic counts (Segments 1 to 8)
INITIAL_COUNTS = [12, 7, 15, 9, 20, 5, 11, 8]
current_traffic = list(INITIAL_COUNTS)


def invoke_cpp(args):
    """
    Executes compiled C++ binary with specified CLI arguments.
    Returns (status_code, parsed_json_or_error_dict).
    """
    if not CPP_EXE.is_file():
        return 500, {
            "success": False,
            "error": f"C++ executable not found at {CPP_EXE}. Please compile src/main.cpp first."
        }

    cmd = [str(CPP_EXE)] + [str(a) for a in args]
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        stdout = proc.stdout.strip()
        if not stdout:
            return 500, {
                "success": False,
                "error": f"C++ binary returned empty output. Stderr: {proc.stderr.strip()}"
            }
        try:
            data = json.loads(stdout)
            return 200 if data.get("success", False) else 400, data
        except json.JSONDecodeError:
            return 500, {
                "success": False,
                "error": f"Failed to parse C++ JSON output: {stdout}"
            }
    except subprocess.TimeoutExpired:
        return 504, {"success": False, "error": "C++ execution timed out"}
    except Exception as e:
        return 500, {"success": False, "error": str(e)}


class FlowGridRequestHandler(SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler serving static dashboard files from app/
    and handling /api/* routes via C++ Fenwick Tree invocation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def end_headers(self):
        # Enable CORS for local cross-origin development/testing
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _send_json(self, status_code, data):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0:
            return {}
        raw = self.wfile if False else self.rfile.read(content_len)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # API: Status & health check
        if path == "/api/status":
            self._send_json(200, {
                "status": "online",
                "backend": "C++ Fenwick Tree (BIT) Core",
                "binary": str(CPP_EXE),
                "binary_exists": CPP_EXE.is_file(),
                "counts": current_traffic
            })
            return

        # API: Current state & BIT array
        if path == "/api/state":
            code, data = invoke_cpp(["--state"] + current_traffic)
            self._send_json(code, data)
            return

        # Serve / as /index.html
        if path == "/":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        global current_traffic
        parsed = urlparse(self.path)
        path = parsed.path

        body = self._read_json_body()
        if body is None:
            self._send_json(400, {"success": False, "error": "Invalid JSON body"})
            return

        # API: Range Query & Congestion Detection
        if path == "/api/query":
            try:
                left = int(body.get("left", 3))
                right = int(body.get("right", 6))
                threshold = int(body.get("threshold", 55))
            except (ValueError, TypeError):
                self._send_json(400, {"success": False, "error": "Range and threshold parameters must be integers"})
                return

            if left < 1 or right > len(current_traffic) or left > right:
                self._send_json(400, {
                    "success": False,
                    "error": f"Invalid range [{left}..{right}]. Bounds must satisfy 1 <= left <= right <= {len(current_traffic)}."
                })
                return

            code, data = invoke_cpp(["--query", left, right, threshold] + current_traffic)
            self._send_json(code, data)
            return

        # API: Point Update
        if path == "/api/update":
            try:
                segment = int(body.get("segment", 0))
                new_count = int(body.get("newCount", 0))
            except (ValueError, TypeError):
                self._send_json(400, {"success": False, "error": "Segment and newCount parameters must be integers"})
                return

            if segment < 1 or segment > len(current_traffic):
                self._send_json(400, {
                    "success": False,
                    "error": f"Segment index {segment} out of bounds (1..{len(current_traffic)})."
                })
                return

            if new_count < 0:
                self._send_json(400, {
                    "success": False,
                    "error": f"Traffic count cannot be negative: {new_count}."
                })
                return

            code, data = invoke_cpp(["--update", segment, new_count] + current_traffic)
            if code == 200 and data.get("success", False):
                current_traffic = data["counts"]
            self._send_json(code, data)
            return

        # API: Reset to benchmark initial state
        if path == "/api/reset":
            current_traffic = list(INITIAL_COUNTS)
            code, data = invoke_cpp(["--state"] + current_traffic)
            if code == 200:
                data["message"] = "State reset to benchmark initial counts"
            self._send_json(code, data)
            return

        self._send_json(404, {"success": False, "error": f"Unknown endpoint: {path}"})


def run_server(port=8000, host="127.0.0.1"):
    server_address = (host, port)
    httpd = HTTPServer(server_address, FlowGridRequestHandler)
    print(f"=" * 70)
    print(f"  FLOWGRID — Dynamic Traffic Analytics Backend Server")
    print(f"  Data Structures & Algorithms (2nd Year CSE Case Study)")
    print(f"=" * 70)
    print(f"  Backend C++ Binary : {CPP_EXE} ({'FOUND' if CPP_EXE.is_file() else 'MISSING'})")
    print(f"  Dashboard URL      : http://{host}:{port}/")
    print(f"  API Endpoints      : /api/status, /api/state, /api/query, /api/update, /api/reset")
    print(f"=" * 70)
    print(f"  Press Ctrl+C to terminate the server.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Shutting down gracefully...")
        httpd.server_close()


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port=port)
