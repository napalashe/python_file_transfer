import socket
import os



def main():
    SERVER_NAME = 'localhost'
    SERVER_PORT = 12000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_NAME, SERVER_PORT))
    
    try:
        while True:
            command = input("ftp> ")
            if not command:
                continue

            client_socket.send(command.encode())

            if command.startswith('GET'):
                handle_get(client_socket, command.split()[1])
            elif command.startswith('PUT'):
                handle_put(client_socket, command.split()[1])
            elif command == 'LS':
                handle_ls(client_socket)
            elif command == 'QUIT':
                print(client_socket.recv(1024).decode())
                break
            else:
                print(client_socket.recv(1024).decode())
    finally:
        client_socket.close()
        print("Connection closed")

def handle_get(client_socket, filename):
    header = client_socket.recv(1024).decode()
    if header.startswith('ERROR'):
        print(header)
    else:
        filesize = int(header.split()[1])
        with open(filename, 'wb') as file:
            remaining = filesize
            while remaining > 0:
                chunk = client_socket.recv(min(1024, remaining))
                if not chunk:
                    break
                file.write(chunk)
                remaining -= len(chunk)
        print("-------------------------------------")
        print(f"Succesfully Downloaded {filename}")

def handle_put(client_socket, filename):
    try:
        filesize = os.path.getsize(filename)
        client_socket.sendall(f"START {filesize}".encode())
        with open(filename, 'rb') as file:
            while (chunk := file.read(1024)):
                client_socket.sendall(chunk)
        print("------------------------------------")
        print(f"Succesfully Uploaded {filename}")
    except FileNotFoundError:
        print("ERROR: File not found.")

def handle_ls(client_socket):
    response = client_socket.recv(4096)
    print("Directory list:")
    print(response.decode())

if __name__ == "__main__":
    main()