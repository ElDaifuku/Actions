import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtCore import Qt
import unittest
from unittest.mock import patch

from main import MyTestApp

app = QApplication(sys.argv)
window = MyTestApp(app)


class TestUIElements(unittest.TestCase):

    def test_button_colors(self):
        expected_button_color = QPalette().button().color()
        actual_button_color = window.button_ipv4_info.palette().button().color()
        self.assertEqual(expected_button_color, actual_button_color)

    def test_button_font_size(self):
        expected_font_size = QFont().pointSize()
        actual_font_size = window.button_ipv4_info.font().pointSize()
        self.assertEqual(expected_font_size, actual_font_size)

    def test_text_output_font_size(self):
        expected_font_size = QFont().pointSize()
        actual_font_size = window.text_output.font().pointSize()
        self.assertEqual(expected_font_size, actual_font_size)

    def test_ipv4_info(self):
        with patch('socket.gethostname', return_value='test_host'):
            with patch('socket.gethostbyname', return_value='127.0.0.1'):
                with patch('psutil.net_if_addrs', return_value={'Wi-Fi': [{'family': 2, 'address': '127.0.0.1'}]}):
                    with patch('socket.gethostbyaddr', return_value=('test_host', [], [])):
                        app = QApplication([])
                        window = MyTestApp(app)
                        window.get_ipv4_info()
                        text_output = window.text_output.toPlainText()
                        self.assertIn("IP: 127.0.0.1", text_output)
                        self.assertIn("Statyczne", text_output)
                        self.assertIn("Interface: Wi-Fi", text_output)
                        app.quit()

    def test_system_info(self):
        with patch('platform.platform', return_value='Windows-10-10.0.19041-SP0'):
            with patch('platform.architecture', return_value=('32bit', 'WindowsPE')):
                with patch('psutil.cpu_count', return_value=4):
                    with patch('psutil.virtual_memory', return_value=psutil._common.svmem(total=4294967296)):
                        app = QApplication([])
                        window = MyTestApp(app)
                        window.get_system_info()
                        text_output = window.text_output.toPlainText()
                        self.assertIn("Wersja SO: Windows-10-10.0.19041-SP0", text_output)
                        self.assertIn("Typ Systemu: ('32bit', 'WindowsPE')", text_output)
                        self.assertIn("Rdzenie: 4", text_output)
                        self.assertIn("RAM: 4.0 GB", text_output)
                        app.quit()

    def test_bios_info(self):
        with patch('wmi.WMI.Win32_BIOS', return_value=[type('obj', (object,), {'Version': 'test_version'})]):
            app = QApplication([])
            window = MyTestApp(app)
            window.get_bios_info()
            text_output = window.text_output.toPlainText()
            self.assertIn("Wersja Biosu: test_version", text_output)
            app.quit()

    def test_hostname(self):
        with patch('socket.gethostname', return_value='test_host'):
            app = QApplication([])
            window = MyTestApp(app)
            window.get_hostname()
            text_output = window.text_output.toPlainText()
            self.assertIn("Nazwa Hosta: test_host", text_output)
            app.quit()


if __name__ == '__main__':
    unittest.main()


