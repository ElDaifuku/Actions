import unittest
from PyQt5.QtWidgets import QApplication
from main import MyTestApp  # Zastąp 'your_module_name' nazwą modułu, w którym znajduje się klasa MyTestApp

class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])

    def tearDown(self):
        self.app.exit()

    def test_ipv4_info(self):
        window = MyTestApp(self.app)
        window.get_ipv4_info()
        text_output = window.text_output.toPlainText()
        self.assertIn("IP:", text_output)
        self.assertIn("Statyczne", text_output)
        self.assertIn("Interfejs:", text_output)

    def test_system_info(self):
        window = MyTestApp(self.app)
        window.get_system_info()
        text_output = window.text_output.toPlainText()
        self.assertIn("Wersja SO:", text_output)
        self.assertIn("Typ Systemu:", text_output)
        self.assertIn("Rdzenie:", text_output)
        self.assertIn("RAM:", text_output)

    def test_bios_info(self):
        window = MyTestApp(self.app)
        window.get_bios_info()
        text_output = window.text_output.toPlainText()
        self.assertIn("Wersja Biosu:", text_output)

    def test_hostname(self):
        window = MyTestApp(self.app)
        window.get_hostname()
        text_output = window.text_output.toPlainText()
        self.assertIn("Nazwa Hosta:", text_output)

if __name__ == '__main__':
    unittest.main()



