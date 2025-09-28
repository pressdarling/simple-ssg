"""Development server for Simple-SSG.

This module provides a simple, local development server for previewing the
generated static site. It uses Python's built-in `http.server` to serve
files from a specified directory.

The server can be started via the `serve` command in the CLI. It also includes
functionality to automatically open a web browser to the correct address.
"""

import os
import http.server
import socketserver
import webbrowser
import threading
import time


def serve(directory: str, port: int = 8000, open_browser: bool = True) -> None:
    """Starts a local development server to preview the static site.

    This function changes the current working directory to the specified one
    and starts a simple HTTP server on the given port. It can also open a new
    browser tab to the server's address.

    Args:
        directory: The root directory from which to serve files (e.g., 'build').
        port: The port number on which the server will listen.
        open_browser: If True, a web browser will be opened to the server's
                      address automatically.
    """
    # Normalize directory path
    directory = os.path.abspath(directory)

    if not os.path.exists(directory):
        print(f"Error: Directory {directory} does not exist.")
        return

    # Change to the directory
    os.chdir(directory)

    # Create handler
    handler = http.server.SimpleHTTPRequestHandler

    try:
        # Try to create the server
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Server started at http://localhost:{port}")
            print(f"Serving files from: {directory}")
            print("Press Ctrl+C to stop")

            # Open browser in a separate thread
            if open_browser:
                threading.Thread(target=lambda: open_browser_delayed(port)).start()

            # Start server
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"Error: Port {port} is already in use. Try a different port.")
        else:
            print(f"Error starting server: {str(e)}")
    except KeyboardInterrupt:
        print("\nServer stopped")


def open_browser_delayed(port: int) -> None:
    """Opens a web browser to the specified port after a short delay.

    This function is run in a separate thread to prevent it from blocking the
    main server thread. The delay gives the server a moment to initialize
    before the browser tries to connect.

    Args:
        port: The port number to open in the browser.
    """
    time.sleep(0.5)  # Wait for server to start
    webbrowser.open(f"http://localhost:{port}")
