import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG)


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор ANSI-кодировки")
        self.setup_ui()

    def setup_ui(self):
        self.hex_label = QLabel("Шестнадцатеричная строка:")
        self.hex_text = QLineEdit()
        self.ansi_label = QLabel("ANSI-кодировка:")
        self.ansi_text = QLineEdit()

        self.hex_text.textChanged.connect(self.convert_to_ansi)
        self.ansi_text.textChanged.connect(self.convert_to_hex)

        layout = QVBoxLayout()
        layout.addWidget(self.hex_label)
        layout.addWidget(self.hex_text)
        layout.addWidget(self.ansi_label)
        layout.addWidget(self.ansi_text)

        self.setLayout(layout)

    def convert_to_ansi(self):
        hex_string = self.hex_text.text()

        try:
            # Конвертирование шестнадцатеричной строки в ANSI-кодировку
            ansi_bytes = bytes.fromhex(hex_string)
            ansi_string = ansi_bytes.decode('cp1251')

            self.ansi_text.setText(ansi_string)
        except Exception as e:
            logging.exception("Ошибка при конвертации в ANSI:")

    def convert_to_hex(self):
        ansi_string = self.ansi_text.text()

        try:
            # Конвертирование ANSI-кодировки в шестнадцатеричную строку
            ansi_bytes = ansi_string.encode('cp1251')
            hex_string = ' '.join(['{:02x}'.format(byte) for byte in ansi_bytes])

            self.hex_text.setText(hex_string)
        except Exception as e:
            logging.exception("Ошибка при конвертации в шестнадцатеричную строку:")


if __name__ == "__main__":
    app = QApplication([])
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
