
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
            path=request[0].split(" ")[1] 
            response=b"HTTP/1.1 404 Not Found\r\n\r\n"          
            if path=="/":
                connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

            elif "/echo/" in path:
                str=path[(len(path)-6):]
                response=f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str)}\r\n\r\n{str}".encode()

            
            else:
                response=b"HTTP/1.1 404 Not Found\r\n\r\n"
            connection.sendall(response)
            connection.close()


            


if __name__ == "__main__":
    main()
