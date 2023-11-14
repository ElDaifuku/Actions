from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtCore import QCoreApplication
from unittest.mock import patch, MagicMock
from PyQt5 import QtWidgets

try:
    import psutil
except ImportError:
    psutil = MagicMock()

from main import MyTestApp


def test_button_colors():
    app = QApplication([])
    window = MyTestApp(app)
    expected_button_color = QPalette().button().color()
    actual_button_color = window.button_ipv4_info.palette().button().color()
    assert expected_button_color == actual_button_color
    app.quit()


def test_button_font_size():
    app = QApplication([])
    window = MyTestApp(app)
    expected_font_size = QFont().pointSize()
    actual_font_size = window.button_ipv4_info.font().pointSize()
    assert expected_font_size == actual_font_size
    app.quit()


def test_text_output_font_size():
    app = QApplication([])
    window = MyTestApp(app)
    expected_font_size = QFont().pointSize()
    actual_font_size = window.text_output.font().pointSize()
    assert expected_font_size == actual_font_size
    app.quit()




def test_system_info():
    with patch('platform.platform', return_value='Windows-10-10.0.19041-SP0'):
        with patch('platform.architecture', return_value=('32bit', 'WindowsPE')):
            with patch('psutil.cpu_count', return_value=4):
                with patch('psutil.virtual_memory', return_value=MagicMock(total=4294967296)):
                    app = QApplication([])
                    window = MyTestApp(app)
                    window.get_system_info()
                    text_output = window.text_output.toPlainText()
                    assert "Wersja SO: Windows-10-10.0.19041-SP0" in text_output
                    assert "Typ Systemu: ('32bit', 'WindowsPE')" in text_output
                    assert "Rdzenie: 4" in text_output
                    assert "RAM: 4.0 GB" in text_output
                    app.quit()




def test_hostname():
    with patch('socket.gethostname', return_value='test_host'):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_hostname()
        text_output = window.text_output.toPlainText()
        assert "Nazwa Hosta: test_host" in text_output
        app.quit()



