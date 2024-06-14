
import socket


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection,address=server_socket.accept()
    connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    connection.close()


if __name__ == "__main__":
    main()
