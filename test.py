from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtTest import QTest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from main import MyTestApp





try:
    import psutil
except ImportError:
    psutil = MagicMock()


def app():
    application = QApplication([])
    yield application
    application.quit()

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


def test_bios_info():
    with patch('wmi.WMI', return_value=MagicMock(Win32_BIOS=[MagicMock(Version='test_version')])):
        app = QApplication([])

        window = MyTestApp(app)

        QTest.qWaitForWindowExposed(window)  # Wait for the window to be exposed

        # Modify the get_bios_info method to handle the list directly
        def mock_Win32_BIOS():
            return [MagicMock(Version='test_version')]

        with patch('wmi.WMI', return_value=MagicMock(Win32_BIOS=mock_Win32_BIOS)):
            window.get_bios_info()

        text_output = window.text_output.toPlainText()

        assert "Wersja Biosu: test_version" in text_output

        app.quit()



def test_hostname():
    with patch('socket.gethostname', return_value='test_host'):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_hostname()
        text_output = window.text_output.toPlainText()
        assert "Nazwa Hosta: test_host" in text_output
        app.quit()





