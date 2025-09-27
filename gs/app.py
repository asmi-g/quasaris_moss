import tkinter as tk
from tkinter import scrolledtext
import threading
from socket import socket, AF_INET, SOCK_DGRAM

class GroundStationGUI:
    def __init__(self, root, udp_ip='127.0.0.1', udp_port=5005):
        self.root = root
        self.root.title("Student Ground Station")
        self.root.geometry("700x500")

        self.udp_ip = udp_ip
        self.udp_port = udp_port

        # --- GUI Layout ---

        # Input
        self.input_label = tk.Label(root, text="Command Input:")
        self.input_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.command_entry = tk.Entry(root, width=50)
        self.command_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.command_entry.bind("<Return>", self.send_command)

        self.send_button = tk.Button(root, text="Send", command=self.send_command)
        self.send_button.grid(row=0, column=2, padx=10, pady=5)

        # Output
        self.output_label = tk.Label(root, text="Ground Station Output:")
        self.output_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.output_text = scrolledtext.ScrolledText(root, width=80, height=25, wrap=tk.WORD, state='disabled')
        self.output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        # Start UDP listener in background
        self.start_udp_server()

    def send_command(self, event=None):
        command = self.command_entry.get().strip()
        if command:
            self.display_output(f"> Sent: {command}")
            # Optional: send to a UDP client here
            self.command_entry.delete(0, tk.END)

    def display_output(self, message):
        self.output_text.configure(state='normal')
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.configure(state='disabled')
        self.output_text.see(tk.END)

    def start_udp_server(self):
        def udp_listener():
            with socket(AF_INET, SOCK_DGRAM) as server_socket:
                try:
                    server_socket.bind((self.udp_ip, self.udp_port))
                except Exception as e:
                    self.display_output(f"[ERROR] Could not bind UDP socket: {e}")
                    return

                self.display_output(f"UDP server listening on {self.udp_ip}:{self.udp_port}")
                while True:
                    try:
                        data, addr = server_socket.recvfrom(1024)
                        message = data.decode('utf-8')
                        display_msg = f"< Received from {addr[0]}:{addr[1]}: {message}"
                        self.root.after(0, self.display_output, display_msg)
                        # Echo back to client
                        server_socket.sendto("Message received".encode(), addr)
                    except Exception as e:
                        self.root.after(0, self.display_output, f"[ERROR] UDP server error: {e}")
                        break

        # Start thread
        udp_thread = threading.Thread(target=udp_listener, daemon=True)
        udp_thread.start()

# --- MAIN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GroundStationGUI(root, udp_ip='127.0.0.1', udp_port=5005)
    root.mainloop()
