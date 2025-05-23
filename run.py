from shop import app
import socket
import os

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
        print(f"Starting SecureCart application on port {port-1} with debug={debug_mode}")
        app.run(debug=debug_mode, host='0.0.0.0', port=port)
    else:
        print("Error: No available ports found. Application cannot start.")
        print("Please ensure ports 5000-5009 are available.")