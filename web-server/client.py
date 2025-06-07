import socket
import sys

def http_client(server_host, server_port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, int(server_port)))

    request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
    client_socket.send(request.encode())

    response = b""
    while True:
        part = client_socket.recv(1024)
        if not part:
            break
        response += part

    print("Response from server:\n")
    print(response.decode(errors='ignore'))
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
        sys.exit(1)

    _, host, port, file = sys.argv
    http_client(host, port, file)
# Example usage: python client.py localhost 6789 index.html