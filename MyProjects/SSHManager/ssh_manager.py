import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import paramiko
from threading import Thread
import queue
import time


class SSHTerminal(tk.Toplevel):
    def __init__(self, parent, client):
        super().__init__(parent)
        self.title("SSH Terminal")
        self.client = client
        self.channel = None
        self.running = False

        self.output_queue = queue.Queue()
        self.create_widgets()
        self.start_ssh_session()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

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
                time.sleep(0.1)
            except:
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
        except:
            messagebox.showerror("Ошибка", "Соединение разорвано")
            self.on_close()

    def on_close(self):
        self.running = False
        if self.channel:
            self.channel.close()
        self.client.close()
        self.destroy()


class SSHSessionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Session Manager")
        self.sessions = {}
        self.load_sessions()
        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="Новая сессия")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Хост:").grid(row=1, column=0, sticky="w")
        self.host_entry = ttk.Entry(input_frame)
        self.host_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Порт:").grid(row=2, column=0, sticky="w")
        self.port_entry = ttk.Entry(input_frame)
        self.port_entry.insert(0, "22")
        self.port_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Пользователь:").grid(row=3, column=0, sticky="w")
        self.user_entry = ttk.Entry(input_frame)
        self.user_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(input_frame, text="Пароль:").grid(row=4, column=0, sticky="w")
        self.password_entry = ttk.Entry(input_frame, show="*")
        self.password_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Button(btn_frame, text="Сохранить", command=self.save_session).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Подключиться", command=self.connect_ssh).pack(side=tk.LEFT, padx=2)

        self.session_list = ttk.Treeview(self.root, columns=("Host", "User"), show="headings")
        self.session_list.heading("Host", text="Хост")
        self.session_list.heading("User", text="Пользователь")
        self.session_list.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.update_session_list()
        self.session_list.bind("<<TreeviewSelect>>", self.load_selected_session)

    def save_session(self):
        session_data = {
            "host": self.host_entry.get(),
            "port": self.port_entry.get(),
            "user": self.user_entry.get(),
            "password": self.password_entry.get()
        }

        session_name = self.name_entry.get()

        if not session_name or not session_data["host"] or not session_data["user"]:
            messagebox.showwarning("Ошибка", "Заполните обязательные поля (Название, Хост, Пользователь)")
            return

        self.sessions[session_name] = session_data
        self.save_to_file()
        self.update_session_list()
        messagebox.showinfo("Успех", "Сессия сохранена!")

    def connect_ssh(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        user = self.user_entry.get()
        password = self.password_entry.get()

        if not host or not user:
            messagebox.showwarning("Ошибка", "Заполните обязательные поля (Хост, Пользователь)")
            return

        Thread(target=self._connect_ssh, args=(host, port, user, password), daemon=True).start()

    def _connect_ssh(self, host, port, user, password):
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
            self.root.after(0, lambda: SSHTerminal(self.root, client))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться: {str(e)}")

    def update_session_list(self):
        self.session_list.delete(*self.session_list.get_children())
        for name, data in self.sessions.items():
            self.session_list.insert("", "end", values=(data["host"], data["user"]), text=name)

    def load_selected_session(self, event):
        selected_item = self.session_list.selection()
        if selected_item:
            session_name = self.session_list.item(selected_item[0], "text")
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
                self.password_entry.insert(0, session_data["password"])

    def save_to_file(self):
        with open("sessions.json", "w") as f:
            json.dump(self.sessions, f)

    def load_sessions(self):
        try:
            with open("sessions.json", "r") as f:
                self.sessions = json.load(f)
        except FileNotFoundError:
            self.sessions = {}


if __name__ == "__main__":
    root = tk.Tk()
    app = SSHSessionManager(root)
    root.mainloop()