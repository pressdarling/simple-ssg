"""
Development server for Simple-SSG.
"""

import os
import http.server
import socketserver
import webbrowser
import threading
import time

def serve(directory, port=8000, open_browser=True):
    """
    Start a development server to preview the site.
    
    Parameters:
    - directory: The directory to serve
    - port: Server port (default: 8000)
    - open_browser: Whether to open a browser (default: True)
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

def open_browser_delayed(port):
    """Open browser after a short delay."""
    time.sleep(0.5)  # Wait for server to start
    webbrowser.open(f"http://localhost:{port}")
