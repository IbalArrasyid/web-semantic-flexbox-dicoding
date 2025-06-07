import socket
import threading
import os

# Server sederhana untuk menangani permintaan HTTP GET
# Menggunakan threading untuk menangani beberapa koneksi secara bersamaan
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Konfigurasi server
HOST = ''  # listen pada semua alamat IP
PORT = 6789  # port yang digunakan

def get_content_type(filename):
    if filename.endswith(".html"):
        return "text/html"
    elif filename.endswith(".css"):
        return "text/css"
    elif filename.endswith(".js"):
        return "application/javascript"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        return "image/jpeg"
    elif filename.endswith(".png"):
        return "image/png"
    else:
        return "application/octet-stream"


def handle_client(connection_socket, client_address):
    try:
        message = connection_socket.recv(1024).decode()
        if not message:
            return

        # Mendapatkan path file dari request
        request_path = message.split()[1]
        if request_path == '/':
            request_path = '/index.html'

        filename = request_path.lstrip('/')  # Hapus leading slash
        full_path = os.path.join(BASE_DIR, filename)

        if os.path.exists(full_path) and os.path.isfile(full_path):
            with open(full_path, 'rb') as f:
                output_data = f.read()

            content_type = get_content_type(filename)

            header = 'HTTP/1.1 200 OK\r\n'
            header += f'Content-Type: {content_type}\r\n'
            header += f'Content-Length: {len(output_data)}\r\n'
            header += 'Connection: close\r\n\r\n'

            connection_socket.sendall(header.encode() + output_data)

        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
            connection_socket.sendall(response.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server running on port {PORT}...")

    while True:
        connection_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
