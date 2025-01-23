import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import paramiko
from threading import Thread
import queue
import time
from cryptography.fernet import Fernet
import os
import datetime


class SecurityManager:
    def __init__(self):
        self.key = None
        self.cipher = None
        self.load_or_create_key()

    def load_or_create_key(self):
        key_file = "secret.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, data):
        return self.cipher.decrypt(data.encode()).decode()


class SSHTerminal(tk.Toplevel):
    def __init__(self, parent, client, session_name):
        super().__init__(parent)
        self.title(f"SSH Terminal - {session_name}")
        self.client = client
        self.channel = None
        self.running = False
        self.session_name = session_name
        self.log_file = None

        self.output_queue = queue.Queue()
        self.setup_logging()
        self.create_widgets()
        self.start_ssh_session()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_logging(self):
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_name = "".join(c if c.isalnum() else "_" for c in self.session_name)
        self.log_filename = f"logs/{safe_name}_{timestamp}.log"
        try:
            self.log_file = open(self.log_filename, 'w', encoding='utf-8')
        except Exception as e:
            messagebox.showerror("Log Error", f"Failed to create log file: {str(e)}")

    def create_widgets(self):
        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        self.input_entry = ttk.Entry(self)
        self.input_entry.pack(fill=tk.X, pady=5)
        self.input_entry.bind("<Return>", self.send_command)
        self.input_entry.focus_set()

    def start_ssh_session(self):
        self.channel = self.client.invoke_shell()
        self.running = True
        Thread(target=self.read_output, daemon=True).start()
        self.after(100, self.update_output)

    def read_output(self):
        while self.running:
            try:
                if self.channel.recv_ready():
                    data = self.channel.recv(1024).decode("utf-8", errors="ignore")
                    self.output_queue.put(data)
                    if self.log_file:
                        self.log_file.write(data)
                        self.log_file.flush()
                time.sleep(0.1)
            except Exception as e:
                print(f"Read error: {str(e)}")
                break

    def update_output(self):
        while not self.output_queue.empty():
            data = self.output_queue.get()
            self.output_text.insert(tk.END, data)
            self.output_text.see(tk.END)
        self.after(100, self.update_output)

    def send_command(self, event):
        cmd = self.input_entry.get() + "\n"
        self.input_entry.delete(0, tk.END)
        try:
            self.channel.send(cmd)
            if self.log_file:
                self.log_file.write(cmd)
                self.log_file.flush()
        except Exception as e:
            messagebox.showerror("Error", f"Connection lost: {str(e)}")
            self.on_close()

    def on_close(self):
        self.running = False
        if self.channel:
            self.channel.close()
        self.client.close()
        if self.log_file:
            self.log_file.close()
        self.destroy()


class SSHSessionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Session Manager")
        self.security = SecurityManager()
        self.sessions = {}
        self.load_sessions()
        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="New Session")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        fields = [
            ("Name:", "name_entry"),
            ("Host:", "host_entry"),
            ("Port:", "port_entry"),
            ("User:", "user_entry"),
            ("Password:", "password_entry")
        ]

        for row, (label, var) in enumerate(fields):
            ttk.Label(input_frame, text=label).grid(row=row, column=0, sticky="w")
            entry = ttk.Entry(input_frame, show="*" if "password" in var else "")
            entry.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
            setattr(self, var, entry)

        self.port_entry.insert(0, "22")

        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Button(btn_frame, text="Save", command=self.save_session).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Connect", command=self.connect_ssh).pack(side=tk.LEFT, padx=2)

        self.session_list = ttk.Treeview(self.root, columns=("Host", "User"), show="headings")
        self.session_list.heading("Host", text="Host")
        self.session_list.heading("User", text="User")
        self.session_list.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.update_session_list()
        self.session_list.bind("<<TreeviewSelect>>", self.load_selected_session)

    def save_session(self):
        session_data = {
            "host": self.host_entry.get(),
            "port": self.port_entry.get(),
            "user": self.user_entry.get(),
            "password": self.security.encrypt(self.password_entry.get())
        }

        session_name = self.name_entry.get()

        if not all([session_name, session_data["host"], session_data["user"]]):
            messagebox.showwarning("Error", "Please fill all required fields (Name, Host, User)")
            return

        self.sessions[session_name] = session_data
        self.save_to_file()
        self.update_session_list()
        messagebox.showinfo("Success", "Session saved!")

    def connect_ssh(self):
        session_name = self.name_entry.get()
        host = self.host_entry.get()
        port = int(self.port_entry.get() or 22)
        user = self.user_entry.get()
        password = self.password_entry.get()

        if not all([session_name, host, user]):
            messagebox.showwarning("Error", "Please fill all required fields (Name, Host, User)")
            return

        Thread(target=self._connect_ssh, args=(host, port, user, password, session_name), daemon=True).start()

    def _connect_ssh(self, host, port, user, password, session_name):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=host,
                port=port,
                username=user,
                password=password,
                look_for_keys=False
            )
            self.root.after(0, lambda: SSHTerminal(self.root, client, session_name))
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")

    def update_session_list(self):
        self.session_list.delete(*self.session_list.get_children())
        for name, data in self.sessions.items():
            self.session_list.insert("", "end", values=(data["host"], data["user"]), text=name)

    def load_selected_session(self, event):
        selected = self.session_list.selection()
        if selected:
            session_name = self.session_list.item(selected[0], "text")
            session_data = self.sessions.get(session_name)
            if session_data:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, session_name)
                self.host_entry.delete(0, tk.END)
                self.host_entry.insert(0, session_data["host"])
                self.port_entry.delete(0, tk.END)
                self.port_entry.insert(0, session_data["port"])
                self.user_entry.delete(0, tk.END)
                self.user_entry.insert(0, session_data["user"])
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, self.security.decrypt(session_data["password"]))

    def save_to_file(self):
        with open("sessions.json", "w") as f:
            json.dump(self.sessions, f)

    def load_sessions(self):
        try:
            with open("sessions.json", "r") as f:
                self.sessions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.sessions = {}


if __name__ == "__main__":
    root = tk.Tk()
    app = SSHSessionManager(root)
    root.mainloop()