from flask import Flask
import socket
import os

app = Flask(__name__)

def get_available_port(max_retries=10):
    for attempt in range(max_retries):
        port = 5000 + attempt
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                s.listen(1)
                return port
        except OSError:
            continue
    return None

if __name__ == '__main__':
    port = get_available_port()
    if port is not None:
        debug_mode = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 'yes']
        print(f"Starting app on port {port} with debug={debug_mode}")
        app.run(debug=debug_mode, host='0.0.0.0', port=port)
    else:
        print("No available ports found.  Application cannot start.")