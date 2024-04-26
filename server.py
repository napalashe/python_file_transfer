import socket
import threading
import os
import sys



def handle_client(connection_socket, ADDR):
    print(f"Connected to {ADDR}")
    try:
        while True:
            command = connection_socket.recv(1024).decode()
            if not command:
                break
            print(f"Received command: {command}")

            if command.startswith('GET'):
                filename = command.split()[1]
                handle_get(connection_socket, filename)
            elif command.startswith('PUT'):
                filename = command.split()[1]
                handle_put(connection_socket, filename)
            elif command == 'LS':
                handle_ls(connection_socket)
            elif command == 'QUIT':
                connection_socket.sendall("Connection closed".encode())
                break
            else:
                connection_socket.sendall("Invalid command".encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection_socket.close()
        print(f"Connection closed for {ADDR}")

def handle_get(connection_socket, filename):
    if os.path.exists(filename):
        connection_socket.sendall(f"START {os.path.getsize(filename)}".encode())
        with open(filename, 'rb') as file:
            while (chunk := file.read(1024)):
                connection_socket.sendall(chunk)
        print(f"Sent {filename}")
    else:
        connection_socket.sendall("ERROR: File not found.".encode())

def handle_put(connection_socket, filename):
    header = connection_socket.recv(1024).decode()
    filesize = int(header.split()[1])
    with open(filename, 'wb') as file:
        remaining = filesize
        while remaining > 0:
            chunk = connection_socket.recv(min(1024, remaining))
            if not chunk:
                break
            file.write(chunk)
            remaining -= len(chunk)
    print(f"Received {filename}")

def handle_ls(connection_socket):
    ls_output = '\n'.join(os.listdir('.')).encode()
    connection_socket.sendall(ls_output)

def main():
    SERVER_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    SERVER_SOCKET.bind(('', SERVER_PORT))
    SERVER_SOCKET.listen(5)
    print(f"The server is ready to receive at port {SERVER_PORT}")

    try:
        while True:
            client_socket, addr = SERVER_SOCKET.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    finally:
        SERVER_SOCKET.close()

if __name__ == "__main__":
    main()