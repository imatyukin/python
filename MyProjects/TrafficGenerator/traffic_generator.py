import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yaml
import socket
import threading
import time
import os
from ipaddress import IPv4Address, ip_address


class TrafficGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Traffic Generator")
        self.geometry("1000x800")
        self.running = False
        self.generator = None
        self.stats = {'sent': 0, 'errors': 0, 'bytes': 0}
        self.history = {'time': [], 'pps': [], 'mbps': []}
        self.start_time = 0

        self.create_widgets()
        self.setup_validations()
        self.load_defaults()
        self.update_stats()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Settings Panel
        settings_frame = ttk.LabelFrame(main_frame, text="Settings")
        settings_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Traffic Type
        ttk.Label(settings_frame, text="Traffic Type:").grid(row=0, column=0, sticky=tk.W)
        self.traffic_type = ttk.Combobox(settings_frame, values=["unicast", "broadcast", "multicast"])
        self.traffic_type.grid(row=0, column=1, pady=2)

        # Network Parameters
        fields = [
            ("Source IP:", "source_ip"),
            ("Destination IP:", "dest_ip"),
            ("Group IP:", "group_ip"),
            ("Source Port:", "source_port"),
            ("Destination Port:", "dest_port"),
            ("Packet Size:", "packet_size"),
            ("Threads:", "threads")
        ]

        for i, (label, var) in enumerate(fields, start=1):
            ttk.Label(settings_frame, text=label).grid(row=i, column=0, sticky=tk.W)
            entry = ttk.Entry(settings_frame)
            entry.grid(row=i, column=1, pady=2)
            setattr(self, var, entry)

        # Speed Control
        speed_frame = ttk.LabelFrame(settings_frame, text="Speed Control")
        speed_frame.grid(row=len(fields) + 1, columnspan=2, pady=5)

        self.speed_mode = tk.StringVar(value="pps")
        modes = [("Packets/sec", "pps"), ("Mbps", "mbps"), ("Interval (s)", "interval")]
        for i, (text, mode) in enumerate(modes):
            ttk.Radiobutton(speed_frame, text=text, variable=self.speed_mode, value=mode).grid(row=0, column=i)

        self.speed_value = ttk.Entry(speed_frame)
        self.speed_value.grid(row=1, columnspan=3)

        # QoS Parameters
        qos_frame = ttk.LabelFrame(settings_frame, text="QoS Parameters")
        qos_frame.grid(row=len(fields) + 2, columnspan=2, pady=5)

        qos_fields = [
            ("DSCP (0-63):", "dscp"),
            ("IP Precedence (0-7):", "ip_prec"),
            ("ECN (0-3):", "ecn")
        ]

        for i, (label, var) in enumerate(qos_fields):
            ttk.Label(qos_frame, text=label).grid(row=i, column=0)
            entry = ttk.Entry(qos_frame, width=8)
            entry.grid(row=i, column=1)
            setattr(self, var, entry)

        # Statistics Panel
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics")
        stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Charts
        fig = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax1 = fig.add_subplot(211)
        self.ax2 = fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(fig, master=stats_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Text Statistics
        self.stats_text = tk.Text(stats_frame, height=4, width=50)
        self.stats_text.pack(fill=tk.X, pady=5)

        # Control Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        self.save_btn = ttk.Button(btn_frame, text="Save Config", command=self.save_config)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.load_btn = ttk.Button(btn_frame, text="Load Config", command=self.load_config)
        self.load_btn.pack(side=tk.LEFT, padx=5)

        self.start_btn = ttk.Button(btn_frame, text="Start", command=self.start_traffic)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_traffic, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Status Bar
        self.status_bar = ttk.Label(self, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, padx=10, pady=5)

    def setup_validations(self):
        validations = {
            self.source_ip: (self.validate_ip, 'focusout'),
            self.dest_ip: (self.validate_ip, 'focusout'),
            self.group_ip: (self.validate_multicast, 'focusout'),
            self.source_port: (self.validate_port, 'focusout'),
            self.dest_port: (self.validate_port, 'focusout'),
            self.packet_size: (self.validate_packet_size, 'focusout'),
            self.threads: (self.validate_threads, 'focusout'),
            self.speed_value: (self.validate_speed, 'key'),
            self.dscp: (lambda v: self.validate_range(v, 0, 63), 'key'),
            self.ip_prec: (lambda v: self.validate_range(v, 0, 7), 'key'),
            self.ecn: (lambda v: self.validate_range(v, 0, 3), 'key')
        }

        for widget, (val_func, event) in validations.items():
            cmd = self.register(val_func)
            widget.configure(validate=event, validatecommand=(cmd, '%P'))

    def load_defaults(self):
        self.traffic_type.set('unicast')
        self.source_ip.insert(0, '0.0.0.0')
        self.dest_ip.insert(0, '192.168.1.100')
        self.group_ip.insert(0, '224.1.1.1')
        self.source_port.insert(0, '0')
        self.dest_port.insert(0, '5060')
        self.packet_size.insert(0, '512')
        self.threads.insert(0, '4')
        self.speed_mode.set('pps')
        self.speed_value.insert(0, '1000')
        self.dscp.insert(0, '0')
        self.ip_prec.insert(0, '0')
        self.ecn.insert(0, '0')

    def validate_ip(self, value):
        try:
            socket.inet_aton(value)
            return True
        except socket.error:
            return False

    def validate_multicast(self, value):
        try:
            return IPv4Address(value).is_multicast
        except ValueError:
            return False

    def validate_port(self, value):
        return value.isdigit() and 0 <= int(value) <= 65535

    def validate_packet_size(self, value):
        return value.isdigit() and 20 <= int(value) <= 65507

    def validate_threads(self, value):
        return value.isdigit() and 1 <= int(value) <= 32

    def validate_speed(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_range(self, value, min_val, max_val):
        if value == "": return True
        if not value.isdigit(): return False
        return min_val <= int(value) <= max_val

    def highlight_field(self, widget, valid):
        bg = 'white' if valid else '#ffdddd'
        widget.config(background=bg)

    def update_stats(self):
        if self.running:
            current_time = time.time() - self.start_time
            self.history['time'].append(current_time)

            # Calculate metrics
            current_sent = self.stats['sent']
            current_bytes = self.stats['bytes']

            if len(self.history['time']) > 1:
                delta = current_time - self.history['time'][-2]
                pps = (current_sent - self.history['pps'][-1]) / delta
                mbps = (current_bytes - self.history['mbps'][-1]) * 8 / delta / 1e6
            else:
                pps = 0
                mbps = 0

            self.history['pps'].append(pps)
            self.history['mbps'].append(mbps)

            # Update charts
            self.ax1.clear()
            self.ax1.plot(self.history['time'], self.history['pps'], label='PPS')
            self.ax1.set_ylabel('Packets/sec')

            self.ax2.clear()
            self.ax2.plot(self.history['time'], self.history['mbps'], label='Mbps', color='orange')
            self.ax2.set_ylabel('Mbps')
            self.ax2.set_xlabel('Time (s)')

            self.canvas.draw()

            # Update text stats
            stats = (f"Total Packets: {self.stats['sent']}\n"
                     f"Errors: {self.stats['errors']}\n"
                     f"Data Sent: {self.stats['bytes'] / 1e6:.2f} MB\n"
                     f"Avg Speed: {self.stats['bytes'] * 8 / (current_time if current_time > 0 else 1) / 1e6:.2f} Mbps")
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, stats)

        self.after(1000, self.update_stats)

    def start_traffic(self):
        if not self.validate_all():
            return

        self.running = True
        self.start_time = time.time()
        self.stats = {'sent': 0, 'errors': 0, 'bytes': 0}
        self.history = {'time': [], 'pps': [], 'mbps': []}

        config = {
            'traffic_type': self.traffic_type.get(),
            'source_address': self.source_ip.get(),
            'source_port': int(self.source_port.get()),
            'destination_address': self.dest_ip.get(),
            'destination_port': int(self.dest_port.get()),
            'group_address': self.group_ip.get(),
            'packet_size': int(self.packet_size.get()),
            'threads': int(self.threads.get()),
            'speed_mode': self.speed_mode.get(),
            'speed_value': self.speed_value.get(),
            'qos': {
                'dscp': int(self.dscp.get()) if self.dscp.get() else None,
                'ip_precedence': int(self.ip_prec.get()) if self.ip_prec.get() else None,
                'ecn': int(self.ecn.get()) if self.ecn.get() else None
            }
        }

        self.generator = TrafficGenerator(config, self.stats)
        self.thread = threading.Thread(target=self.generator.run)
        self.thread.start()

        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_bar.config(text="Generating traffic...")

    def stop_traffic(self):
        self.running = False
        if self.generator:
            self.generator.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_bar.config(text="Ready")

    def validate_all(self):
        checks = [
            (self.validate_ip(self.source_ip.get()), "Invalid Source IP"),
            (self.validate_ip(self.dest_ip.get()), "Invalid Destination IP"),
            (self.traffic_type.get() != 'multicast' or self.validate_multicast(self.group_ip.get()),
             "Invalid Multicast Group"),
            (self.validate_port(self.source_port.get()), "Invalid Source Port"),
            (self.validate_port(self.dest_port.get()), "Invalid Destination Port"),
            (self.validate_packet_size(self.packet_size.get()), "Packet Size must be 20-65507 bytes"),
            (self.validate_threads(self.threads.get()), "Threads must be 1-32"),
            (self.validate_speed(self.speed_value.get()), "Invalid Speed Value")
        ]

        for valid, msg in checks:
            if not valid:
                messagebox.showerror("Validation Error", msg)
                return False
        return True

    def save_config(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        if not file_path:
            return

        config = {
            'traffic_type': self.traffic_type.get(),
            'source_address': self.source_ip.get(),
            'source_port': self.source_port.get(),
            'destination_address': self.dest_ip.get(),
            'destination_port': self.dest_port.get(),
            'group_address': self.group_ip.get(),
            'packet_size': self.packet_size.get(),
            'threads': self.threads.get(),
            'speed_mode': self.speed_mode.get(),
            'speed_value': self.speed_value.get(),
            'qos': {
                'dscp': self.dscp.get(),
                'ip_precedence': self.ip_prec.get(),
                'ecn': self.ecn.get()
            }
        }

        try:
            with open(file_path, 'w') as f:
                yaml.dump(config, f)
            self.status_bar.config(text=f"Config saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def load_config(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)

            self.traffic_type.set(config.get('traffic_type', 'unicast'))
            self.source_ip.delete(0, tk.END)
            self.source_ip.insert(0, config.get('source_address', '0.0.0.0'))
            self.dest_ip.delete(0, tk.END)
            self.dest_ip.insert(0, config.get('destination_address', '192.168.1.100'))
            self.group_ip.delete(0, tk.END)
            self.group_ip.insert(0, config.get('group_address', '224.1.1.1'))
            self.source_port.delete(0, tk.END)
            self.source_port.insert(0, config.get('source_port', '0'))
            self.dest_port.delete(0, tk.END)
            self.dest_port.insert(0, config.get('destination_port', '5060'))
            self.packet_size.delete(0, tk.END)
            self.packet_size.insert(0, config.get('packet_size', '512'))
            self.threads.delete(0, tk.END)
            self.threads.insert(0, config.get('threads', '4'))
            self.speed_mode.set(config.get('speed_mode', 'pps'))
            self.speed_value.delete(0, tk.END)
            self.speed_value.insert(0, config.get('speed_value', '1000'))
            self.dscp.delete(0, tk.END)
            self.dscp.insert(0, config.get('qos', {}).get('dscp', '0'))
            self.ip_prec.delete(0, tk.END)
            self.ip_prec.insert(0, config.get('qos', {}).get('ip_precedence', '0'))
            self.ecn.delete(0, tk.END)
            self.ecn.insert(0, config.get('qos', {}).get('ecn', '0'))

            self.status_bar.config(text=f"Config loaded from {file_path}")
        except Exception as e:
            messagebox.showerror("Load Error", str(e))


class TrafficGenerator:
    def __init__(self, config, stats):
        self.config = config
        self.stats = stats
        self.running = False

    def run(self):
        self.running = True
        threads = []

        for _ in range(self.config['threads']):
            t = threading.Thread(target=self.send_thread)
            t.start()
            threads.append(t)

        while self.running and any(t.is_alive() for t in threads):
            time.sleep(0.1)

    def send_thread(self):
        try:
            sock = self.create_socket()
            dest = self.get_destination()
            data = os.urandom(self.config['packet_size'])
            packet_count = 0
            start_time = time.time()

            while self.running:
                try:
                    sock.sendto(data, dest)
                    packet_count += 1

                    if packet_count % 100 == 0:
                        with threading.Lock():
                            self.stats['sent'] += 100
                            self.stats['bytes'] += 100 * self.config['packet_size']

                    self.adjust_speed(start_time, packet_count)

                except Exception as e:
                    with threading.Lock():
                        self.stats['errors'] += 1

            sock.close()
        except Exception as e:
            with threading.Lock():
                self.stats['errors'] += 1

    def adjust_speed(self, start_time, packet_count):
        if self.config['speed_mode'] == 'pps':
            target = int(self.config['speed_value'])
            expected_time = packet_count / target
            actual_time = time.time() - start_time
            sleep_time = expected_time - actual_time
            if sleep_time > 0:
                time.sleep(sleep_time)
        elif self.config['speed_mode'] == 'interval':
            time.sleep(float(self.config['speed_value']))

    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # QoS Settings
        tos = 0
        if self.config['qos']['dscp'] is not None:
            tos |= (self.config['qos']['dscp'] << 2)
        elif self.config['qos']['ip_precedence'] is not None:
            tos |= (self.config['qos']['ip_precedence'] << 5)
        if self.config['qos']['ecn'] is not None:
            tos |= self.config['qos']['ecn']

        if tos > 0:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, tos)

        # Traffic Type Settings
        if self.config['traffic_type'] == 'broadcast':
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        elif self.config['traffic_type'] == 'multicast':
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        sock.bind((self.config['source_address'], self.config['source_port']))
        return sock

    def get_destination(self):
        if self.config['traffic_type'] == 'multicast':
            return (self.config['group_address'], self.config['destination_port'])
        return (self.config['destination_address'], self.config['destination_port'])


if __name__ == "__main__":
    app = TrafficGeneratorApp()
    app.mainloop()