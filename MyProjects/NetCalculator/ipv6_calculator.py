from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QLabel
)
import ipaddress


class IPv6Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Input field for IPv6 address and prefix
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter IPv6 address/prefix (e.g., 2001:db8::/64)")
        layout.addWidget(self.input_field)

        # Display format selector
        self.display_format = QComboBox()
        self.display_format.addItems(["Compressed", "Expanded"])
        self.display_format.currentIndexChanged.connect(self.update_results)  # Update on format change
        layout.addWidget(QLabel("Display Format:"))
        layout.addWidget(self.display_format)

        # Calculate button
        self.calculate_btn = QPushButton("Calculate Subnet")
        self.calculate_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_btn)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)  # Two columns: Parameter and Value

        # Remove headers
        self.results_table.horizontalHeader().setVisible(False)
        self.results_table.verticalHeader().setVisible(False)

        # Set table rows for parameters
        parameters = [
            "CIDR Notation",
            "Address",
            "Address Range Start",
            "Address Range End",
            "Mask Bits",
            "Usable Addresses",
            "Available Subnets"
        ]
        self.results_table.setRowCount(len(parameters))
        for row, param in enumerate(parameters):
            self.results_table.setItem(row, 0, QTableWidgetItem(param))
            self.results_table.setItem(row, 1, QTableWidgetItem(""))

        # Stretch columns to fit the table width
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.horizontalHeader().setSectionResizeMode(0, self.results_table.horizontalHeader().Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(1, self.results_table.horizontalHeader().Stretch)

        layout.addWidget(self.results_table)
        self.setLayout(layout)

        # Store the last valid network for immediate updates
        self.last_valid_network = None

    def calculate(self):
        input_text = self.input_field.text().strip()

        try:
            # Parse network with strict=False to accept host bits
            network = ipaddress.IPv6Network(input_text, strict=False)
            self.last_valid_network = network  # Save the last valid network
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {str(e)}")
            return

        self.update_results()

    def update_results(self):
        if not self.last_valid_network:
            return

        network = self.last_valid_network
        display_format = self.display_format.currentText()

        try:
            # Format CIDR notation
            cidr_notation = self.format_ipv6(network.with_prefixlen, display_format)
            self.results_table.item(0, 1).setText(cidr_notation)

            # Format Address
            address = self.format_ipv6(str(network.network_address), display_format)
            self.results_table.item(1, 1).setText(address)

            # Format Address Range Start
            range_start = self.format_ipv6(str(network[0]), display_format)
            self.results_table.item(2, 1).setText(range_start)

            # Format Address Range End
            range_end = self.format_ipv6(str(network[-1]), display_format)
            self.results_table.item(3, 1).setText(range_end)

            # Mask Bits
            self.results_table.item(4, 1).setText(f"{network.prefixlen}")

            # Usable Addresses
            usable_addrs = network.num_addresses
            formatted_usable_addrs = f"{usable_addrs:,}"  # Add commas for thousands separator
            self.results_table.item(5, 1).setText(formatted_usable_addrs)

            # Available Subnets
            if network.prefixlen < 128:
                standard_subnet_prefix = 64
                if network.prefixlen <= standard_subnet_prefix:
                    subnets = 2 ** (standard_subnet_prefix - network.prefixlen)
                    formatted_subnets = f"/{standard_subnet_prefix} {subnets} network{'s' if subnets > 1 else ''}"
                else:
                    formatted_subnets = "N/A (prefix too large)"
                self.results_table.item(6, 1).setText(formatted_subnets)
            else:
                self.results_table.item(6, 1).setText("N/A")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Calculation error: {str(e)}")

    def format_ipv6(self, ipv6_str, display_format):
        """
        Formats an IPv6 address based on the selected display format.
        """
        ip = ipaddress.IPv6Address(ipv6_str.split("/")[0])  # Extract IP part if CIDR is present
        if display_format == "Expanded":
            return ip.exploded  # Full representation with leading zeros
        elif display_format == "Compressed":
            return ip.compressed  # Compressed representation
        return ipv6_str


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = IPv6Calculator()
    window.setWindowTitle("IPv6 Calculator")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())