import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PIL import Image

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
            # Проверка на валидность шестнадцатеричной строки
            if all(c in '0123456789ABCDEFabcdef' for c in hex_string):
                # Конвертирование шестнадцатеричной строки в ANSI-кодировку
                ansi_bytes = bytes.fromhex(hex_string)
                ansi_string = ansi_bytes.decode('cp1251')

                self.ansi_text.setText(ansi_string)
            else:
                self.ansi_text.setText("Некорректная шестнадцатеричная строка")
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


class VideoEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактирование видео")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.video_file_label = QLabel("Выберите видеофайл:")
        self.video_file_edit = QLineEdit()
        self.video_file_button = QPushButton("Обзор...")
        self.video_file_button.clicked.connect(self.browse_video_file)

        self.video_duration_label = QLabel("Новая продолжительность (в секундах):")
        self.video_duration_edit = QLineEdit()

        self.video_edit_button = QPushButton("Редактировать")
        self.video_edit_button.clicked.connect(self.edit_video)

        layout.addWidget(self.video_file_label)
        layout.addWidget(self.video_file_edit)
        layout.addWidget(self.video_file_button)
        layout.addWidget(self.video_duration_label)
        layout.addWidget(self.video_duration_edit)
        layout.addWidget(self.video_edit_button)

        self.setLayout(layout)

    def browse_video_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Video Files (*.mp4)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.video_file_edit.setText(file_path)

    def edit_video(self):
        file_path = self.video_file_edit.text()
        duration = self.video_duration_edit.text()
        if not file_path or not duration:
            return

        try:
            duration = int(duration)
            # Здесь должен быть ваш код редактирования видео
            logging.info("Редактирование видео: %s, продолжительность: %d", file_path, duration)
        except ValueError:
            logging.exception("Неверный формат продолжительности видео.")


class FileEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактирование файла")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.file_label = QLabel("Выберите файл:")
        self.file_edit = QLineEdit()
        self.file_button = QPushButton("Обзор...")
        self.file_button.clicked.connect(self.browse_file)

        self.file_size_label = QLabel("Новый размер файла (в байтах):")
        self.file_size_edit = QLineEdit()

        self.file_edit_button = QPushButton("Редактировать")
        self.file_edit_button.clicked.connect(self.edit_file)

        layout.addWidget(self.file_label)
        layout.addWidget(self.file_edit)
        layout.addWidget(self.file_button)
        layout.addWidget(self.file_size_label)
        layout.addWidget(self.file_size_edit)
        layout.addWidget(self.file_edit_button)

        self.setLayout(layout)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("All Files (*)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.file_edit.setText(file_path)

    def edit_file(self):
        file_path = self.file_edit.text()
        size = self.file_size_edit.text()
        if not file_path or not size:
            return

        try:
            size = int(size)
            # Здесь должен быть ваш код редактирования файла
            logging.info("Редактирование файла: %s, размер: %d", file_path, size)
        except ValueError:
            logging.exception("Неверный формат размера файла.")


class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактирование изображения")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.image_file_label = QLabel("Выберите изображение:")
        self.image_file_edit = QLineEdit()
        self.image_file_button = QPushButton("Обзор...")
        self.image_file_button.clicked.connect(self.browse_image_file)

        self.image_width_label = QLabel("Новая ширина изображения (в пикселях):")
        self.image_width_edit = QLineEdit()

        self.image_height_label = QLabel("Новая высота изображения (в пикселях):")
        self.image_height_edit = QLineEdit()

        self.image_edit_button = QPushButton("Редактировать")
        self.image_edit_button.clicked.connect(self.edit_image)

        layout.addWidget(self.image_file_label)
        layout.addWidget(self.image_file_edit)
        layout.addWidget(self.image_file_button)
        layout.addWidget(self.image_width_label)
        layout.addWidget(self.image_width_edit)
        layout.addWidget(self.image_height_label)
        layout.addWidget(self.image_height_edit)
        layout.addWidget(self.image_edit_button)

        self.setLayout(layout)

    def browse_image_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Image Files (*.jpg *.png)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.image_file_edit.setText(file_path)

    def edit_image(self):
        file_path = self.image_file_edit.text()
        width = self.image_width_edit.text()
        height = self.image_height_edit.text()
        if not file_path or not width or not height:
            return

        try:
            width = int(width)
            height = int(height)
            # Здесь должен быть ваш код редактирования изображения
            image = Image.open(file_path)
            image = image.resize((width, height))
            # Сохранение отредактированного изображения
            edited_file_path = f"edited_{file_path}"
            image.save(edited_file_path)
            logging.info("Отредактированное изображение сохранено в: %s", edited_file_path)
        except ValueError:
            logging.exception("Неверный формат ширины или высоты изображения.")
        except Exception as e:
            logging.exception("Ошибка при редактировании изображения.")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мультитул")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        tab_widget = QTabWidget()
        tab_widget.addTab(Calculator(), "Калькулятор ANSI-кодировки")
        tab_widget.addTab(VideoEditor(), "Редактирование видео")
        tab_widget.addTab(FileEditor(), "Редактирование файла")
        tab_widget.addTab(ImageEditor(), "Редактирование изображения")

        layout.addWidget(tab_widget)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
