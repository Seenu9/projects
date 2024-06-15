
import socket


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
         connection,address=server_socket.accept()
         with connection:
            data=connection.recv(1024)
            if not data:
                break
            request=data.decode().split("\r\n")
            request_line=request[0].split(" ")[1]           
            if request_line=="/":
                connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                connection.sendall(b"HTTP/1.1 404 Not Found \r\n\r\n")
            connection.close()


            


if __name__ == "__main__":
    main()
