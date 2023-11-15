import sys
import socket
import platform
import psutil
import wmi
import urllib.request  # Dodajemy import urllib.request
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
from PyQt5.QtCore import Qt
import unittest

class MyTestApp(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Test')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.text_output = QTextEdit(self)
        layout.addWidget(self.text_output)

        self.button_ipv4_info = QPushButton('IPv4', self)
        self.button_proxy_info = QPushButton('Proxy', self)
        self.button_system_info = QPushButton('SO info', self)
        self.button_bios_info = QPushButton('BIOS', self)
        self.button_hostname_info = QPushButton('HOST', self)

        layout.addWidget(self.button_ipv4_info)
        layout.addWidget(self.button_proxy_info)
        layout.addWidget(self.button_system_info)
        layout.addWidget(self.button_bios_info)
        layout.addWidget(self.button_hostname_info)

        central_widget.setLayout(layout)

        self.button_ipv4_info.clicked.connect(self.get_ipv4_info)
        self.button_proxy_info.clicked.connect(self.get_proxy_info)
        self.button_system_info.clicked.connect(self.get_system_info)
        self.button_bios_info.clicked.connect(self.get_bios_info)
        self.button_hostname_info.clicked.connect(self.get_hostname)

    import socket
    import psutil

    def get_ipv4_info(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        # Pobierz listę dostępnych interfejsów sieciowych
        interfaces = psutil.net_if_addrs()

        interface = None
        for iface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address == ip:
                    if "Wi-Fi" in iface:
                        interface = "Wi-Fi"
                    elif "Ethernet" in iface:
                        interface = "Ethernet"

        host_info = socket.gethostbyaddr(ip)
        is_static = "Statyczne" if host_info[0] == hostname else "Dynamiczne"

        result = f"IP: {ip}\n{is_static} IP\nInterfejs: {interface}\n--------------"
        self.text_output.append(result)

    def get_proxy_info(self):
        proxy_handler = urllib.request.ProxyHandler()
        opener = urllib.request.build_opener(proxy_handler)


        try:
            opener.open("http://www.google.com", timeout=5)
            is_proxy_enabled = True
        except Exception:
            is_proxy_enabled = False

        if is_proxy_enabled:
            proxy_status = "Proxy is enabled"
        else:
            proxy_status = "Proxy is disabled"

        result = f"Proxy Status: {proxy_status}\n--------------"
        self.text_output.append(result)

    def get_system_info(self):
        os_version = platform.platform()
        os_architecture = platform.architecture()
        num_cores = psutil.cpu_count(logical=False)
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        result = (f"Wersja SO: {os_version}\nTyp Systemu: {os_architecture}\nRdzenie: {num_cores}\nRAM: {ram} GB"
                  f"\n--------------")
        self.text_output.append(result)

    def get_bios_info(self):
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        result = (f"nWersja Biosu: {bios.Version}"
                  f"\n--------------")
        self.text_output.append(result)

    def get_hostname(self):
        hostname = socket.gethostname()
        self.text_output.append(f"Nazwa Hosta: {hostname}\n--------------")


class Test(unittest.TestCase):
    def test_ipv4_info(self):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_ipv4_info()
        text_output = window.text_output.toPlainText()
        self.assertIn("IP:", text_output)
        self.assertIn("Statyczne:", text_output)
        self.assertIn("Interface:", text_output)
        app.quit()

    def test_system_info(self):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_system_info()
        text_output = window.text_output.toPlainText()
        self.assertIn("Wersja SO:", text_output)
        self.assertIn("Typ systemu:", text_output)
        self.assertIn("Rdzenie:", text_output)
        self.assertIn("RAM:", text_output)
        app.quit()

    def test_bios_info(self):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_bios_info()
        text_output = window.text_output.toPlainText()
        self.assertIn("Wersja Biosu:", text_output)
        app.quit()

    def test_hostname(self):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_hostname()
        text_output = window.text_output.toPlainText()
        self.assertIn("Nazwa Hosta:", text_output)
        app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyTestApp(app)
    window.show()
    sys.exit(app.exec_())


