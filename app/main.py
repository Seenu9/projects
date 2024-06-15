
import socket


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    while True:
         connection,address=server_socket.accept()
         with connection:
            data=connection.recv(1024)
            if not data:
                continue
            request=data.decode().split("\r\n")
            path=request[0].split(" ")[1] 
            response=b"HTTP/1.1 404 Not Found\r\n\r\n"          
            if path=="/":
                connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

            elif path.startswith("/echo/"):
                e_str=path[(len("/echo/")):]
                response=f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(e_str)}\r\n\r\n{e_str}".encode()
            elif path.startswith("/user-agent"):
                useragent=request[2].split(": ")[1]
                response=f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(useragent)}\r\n\r\n{useragent}".encode()
            
            else:
                response=b"HTTP/1.1 404 Not Found\r\n\r\n"
            connection.sendall(response)


            


if __name__ == "__main__":
    main()
