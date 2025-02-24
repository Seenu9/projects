
import socket
import sys
import binascii
import gzip



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
            type=request[0].split(" ")[0]
            req_body=request[-1]
            encoding =[]
            for line in request:
                if line.lower().startswith("accept-encoding:"):
                    encoding =[e.strip() for e in line.split(":")[1].split(",")]
            response=b"HTTP/1.1 404 Not Found\r\n\r\n"
            if type.upper()=="GET" :
                if path=="/":
                    connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

                elif path.startswith("/echo/"):
                    e_str=path[(len("/echo/")):]
                    e_str_comprssed=gzip.compress(e_str.encode("utf-8"))
                    if "gzip" in encoding:
                        response=f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(e_str_comprssed)}\r\n\r\n".encode()+e_str_comprssed               
                    else:
                        response=f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(e_str)}\r\n\r\n{e_str}".encode()
                elif path.startswith("/user-agent"):
                    useragent=request[2].split(": ")[1]
                    response=f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(useragent)}\r\n\r\n{useragent}".encode()
                elif path.startswith("/files"):
                    directory=sys.argv[2]
                    filename=path[len("/files"):]
                    try:
                        with open(f"/{directory}/{filename}","r") as f:
                            body=f.read()
                            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
                    except Exception as e:
                        response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
                else:
                    response=b"HTTP/1.1 404 Not Found\r\n\r\n"
        
            elif type.upper()=="POST":
                if path.startswith("/files"):
                    directo=sys.argv[2]
                    file_n=path[len("/files"):]
                    try:
                        with open(f"/{directo}/{file_n}","w") as fi:
                            fi.write(f"{req_body}")
                            response=f"HTTP/1.1 201 Created\r\n\r\n".encode()
                    except Exception as e:
                        response=b"HTTP/1.1 404 Not Found\r\n\r\n"
            connection.sendall(response)

                        




            


if __name__ == "__main__":
    main()
