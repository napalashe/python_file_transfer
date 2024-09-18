import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class FTPClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("FTP Client")
        self.SERVER_NAME = 'localhost'
        self.SERVER_PORT = 12000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.SERVER_NAME, self.SERVER_PORT))

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.pack(pady=10)

        tk.Label(frame, text="File Name:").grid(row=0, column=0, padx=5, pady=5)
        self.file_name_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.file_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame, text="GET", command=self.handle_get, width=10).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame, text="PUT", command=self.handle_put, width=10).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame, text="LS", command=self.handle_ls, width=10).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(frame, text="QUIT", command=self.handle_quit, width=10).grid(row=2, column=1, padx=5, pady=5)

        self.display_text = scrolledtext.ScrolledText(self.master, width=60, height=20)
        self.display_text.pack(padx=10, pady=10)

    def handle_get(self):
        filename = self.file_name_var.get()
        if filename:
            self.client_socket.send(f'GET {filename}'.encode())
            header = self.client_socket.recv(1024).decode()
            if header.startswith('ERROR'):
                self.display_text.insert(tk.END, f"{header}\n")
            else:
                filesize = int(header.split()[1])
                with open(filename, 'wb') as file:
                    remaining = filesize
                    while remaining > 0:
                        chunk = self.client_socket.recv(min(1024, remaining))
                        if not chunk:
                            break
                        file.write(chunk)
                        remaining -= len(chunk)
                self.display_text.insert(tk.END, f"Successfully Downloaded {filename}\n")
        else:
            messagebox.showwarning("Input Required", "Please enter a file name to download.")

    def handle_put(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            self.client_socket.sendall(f"PUT {filename}".encode())
            self.client_socket.recv(1024)  # Wait for server acknowledgment
            self.client_socket.sendall(f"START {filesize}".encode())
            with open(filepath, 'rb') as file:
                while (chunk := file.read(1024)):
                    self.client_socket.sendall(chunk)
            self.display_text.insert(tk.END, f"Successfully Uploaded {filename}\n")

    def handle_ls(self):
        self.client_socket.send(b'LS')
        response = self.client_socket.recv(4096)
        self.display_text.insert(tk.END, f"Directory list:\n{response.decode()}\n")

    def handle_quit(self):
        self.client_socket.send(b'QUIT')
        self.client_socket.close()
        self.master.destroy()
        messagebox.showinfo("Info", "Connection closed.")

def main():
    root = tk.Tk()
    app = FTPClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
