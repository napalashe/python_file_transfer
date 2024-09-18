import socket
import threading
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

class FTPServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("FTP Server")
        self.SERVER_PORT = 12000
        self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.is_running = False

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.pack(pady=10)

        tk.Label(frame, text="Server Port:").grid(row=0, column=0, padx=5, pady=5)
        self.port_var = tk.StringVar(value=str(self.SERVER_PORT))
        tk.Entry(frame, textvariable=self.port_var, width=10).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame, text="Start Server", command=self.start_server, width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame, text="Stop Server", command=self.stop_server, width=15).grid(row=1, column=1, padx=5, pady=5)

        self.display_text = scrolledtext.ScrolledText(self.master, width=60, height=20)
        self.display_text.pack(padx=10, pady=10)

    def start_server(self):
        if not self.is_running:
            try:
                self.SERVER_PORT = int(self.port_var.get())
                self.SERVER_SOCKET.bind(('', self.SERVER_PORT))
                self.SERVER_SOCKET.listen(5)
                self.is_running = True
                self.display_text.insert(tk.END, f"The server is ready to receive at port {self.SERVER_PORT}\n")
                threading.Thread(target=self.accept_clients, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start server: {e}")
        else:
            messagebox.showinfo("Info", "Server is already running.")

    def stop_server(self):
        if self.is_running:
            self.is_running = False
            self.SERVER_SOCKET.close()
            self.display_text.insert(tk.END, "Server stopped.\n")
        else:
            messagebox.showinfo("Info", "Server is not running.")

    def accept_clients(self):
        try:
            while self.is_running:
                client_socket, addr = self.SERVER_SOCKET.accept()
                self.display_text.insert(tk.END, f"Connected to {addr}\n")
                threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
        except Exception as e:
            if self.is_running:
                self.display_text.insert(tk.END, f"Error accepting clients: {e}\n")

    def handle_client(self, connection_socket, ADDR):
        try:
            while True:
                command = connection_socket.recv(1024).decode()
                if not command:
                    break
                self.display_text.insert(tk.END, f"Received command from {ADDR}: {command}\n")

                if command.startswith('GET'):
                    filename = command.split()[1]
                    self.handle_get(connection_socket, filename, ADDR)
                elif command.startswith('PUT'):
                    filename = command.split()[1]
                    connection_socket.send(b'ACK')  # Send acknowledgment
                    self.handle_put(connection_socket, filename, ADDR)
                elif command == 'LS':
                    self.handle_ls(connection_socket)
                elif command == 'QUIT':
                    connection_socket.sendall("Connection closed".encode())
                    break
                else:
                    connection_socket.sendall("Invalid command".encode())

        except Exception as e:
            self.display_text.insert(tk.END, f"Error with client {ADDR}: {e}\n")
        finally:
            connection_socket.close()
            self.display_text.insert(tk.END, f"Connection closed for {ADDR}\n")

    def handle_get(self, connection_socket, filename, ADDR):
        if os.path.exists(filename):
            connection_socket.sendall(f"START {os.path.getsize(filename)}".encode())
            with open(filename, 'rb') as file:
                while (chunk := file.read(1024)):
                    connection_socket.sendall(chunk)
            self.display_text.insert(tk.END, f"Sent {filename} to {ADDR}\n")
        else:
            connection_socket.sendall("ERROR: File not found.".encode())
            self.display_text.insert(tk.END, f"File not found: {filename}\n")

    def handle_put(self, connection_socket, filename, ADDR):
        header = connection_socket.recv(1024).decode()
        if header.startswith('START'):
            filesize = int(header.split()[1])
            with open(filename, 'wb') as file:
                remaining = filesize
                while remaining > 0:
                    chunk = connection_socket.recv(min(1024, remaining))
                    if not chunk:
                        break
                    file.write(chunk)
                    remaining -= len(chunk)
            self.display_text.insert(tk.END, f"Received {filename} from {ADDR}\n")
        else:
            self.display_text.insert(tk.END, f"Invalid header from {ADDR}: {header}\n")

    def handle_ls(self, connection_socket):
        ls_output = '\n'.join(os.listdir('.')).encode()
        connection_socket.sendall(ls_output)
        self.display_text.insert(tk.END, "Sent directory listing.\n")

def main():
    root = tk.Tk()
    app = FTPServerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
