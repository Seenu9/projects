import socket
import sys
import os


def handle_request(connection):
    data = connection.recv(1024)
    if not data:
        return

    request = data.decode().split("\r\n")
    path = request[0].split(" ")[1]
    method = request[0].split(" ")[0]
    req_body = request[-1]

    # Extract encoding header if it exists
    encoding = None
    for line in request:
        if line.lower().startswith("accept-encoding:"):
            encoding = line.split(":")[1].strip()

    response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    if method.upper() == "GET":
        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo/"):
            e_str = path[len("/echo/"):]
            if encoding == "gzip":
                response = f"HTTP/1.1 200 OK\r\nContent-Encoding: {encoding}\r\nContent-Type: text/plain\r\nContent-Length: {len(e_str)}\r\n\r\n{e_str}".encode()
            else:
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(e_str)}\r\n\r\n{e_str}".encode()
        elif path.startswith("/user-agent"):
            useragent = request[2].split(": ")[1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(useragent)}\r\n\r\n{useragent}".encode()
        elif path.startswith("/files"):
            directory = sys.argv[2]
            filename = path[len("/files/"):]
            safe_filename = os.path.normpath(f"/{directory}/{filename}").lstrip("/")
            if safe_filename.startswith(directory):
                try:
                    with open(safe_filename, "r") as f:
                        body = f.read()
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
                except Exception as e:
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    elif method.upper() == "POST":
        if path.startswith("/files"):
            directory = sys.argv[2]
            filename = path[len("/files/"):]
            safe_filename = os.path.normpath(f"/{directory}/{filename}").lstrip("/")
            if safe_filename.startswith(directory):
                try:
                    with open(safe_filename, "w") as f:
                        f.write(req_body)
                        response = b"HTTP/1.1 201 Created\r\n\r\n"
                except Exception as e:
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    connection.sendall(response)


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    try:
        while True:
            connection, address = server_socket.accept()
            with connection:
                handle_request(connection)
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <port> <directory>")
        sys.exit(1)
    main()
