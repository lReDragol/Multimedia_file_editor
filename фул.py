import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QAction, QFileDialog, QPlainTextEdit, QComboBox
from PyQt5.QtGui import QIcon
from PIL import Image

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Редактор видео и файла")
        self.setGeometry(300, 300, 400, 300)
        self.setWindowIcon(QIcon('icon.png'))

        # Создание главного виджета
        self.main_widget = QWidget(self)

        # Создание компонентов пользовательского интерфейса
        self.file_label = QLabel("Выберите файл:")
        self.file_path_edit = QLineEdit()
        self.browse_button = QAction(QIcon('folder.png'), "Обзор", self)

        self.video_duration_label = QLabel("Введите новую продолжительность (в секундах):")
        self.video_duration_edit = QLineEdit()
        self.edit_video_button = QAction(QIcon('video.png'), "Редактировать видео", self)

        self.file_size_label = QLabel("Изменить размер файла:")
        self.file_size_edit = QLineEdit()
        self.file_size_unit_combobox = QComboBox()
        self.file_size_unit_combobox.addItems(['байты', 'килобайты', 'мегабайты', 'гигабайты', 'терабайты'])
        self.edit_file_size_button = QAction(QIcon('resize.png'), "Редактировать размер файла", self)

        self.result_label = QLabel("Результат:")
        self.result_window = QPlainTextEdit()
        self.result_window.setReadOnly(True)

        # Создание меню
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        edit_menu = menu_bar.addMenu("Редактировать")

        # Добавление действий в меню Файл
        file_menu.addAction(self.browse_button)

        # Добавление действий в меню Редактировать
        edit_menu.addAction(self.edit_video_button)
        edit_menu.addAction(self.edit_file_size_button)

        # Размещение компонентов на главном виджете
        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_path_edit)
        layout.addWidget(self.video_duration_label)
        layout.addWidget(self.video_duration_edit)
        layout.addWidget(self.file_size_label)
        layout.addWidget(self.file_size_edit)
        layout.addWidget(self.file_size_unit_combobox)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_window)
        self.main_widget.setLayout(layout)

        # Установка главного виджета
        self.setCentralWidget(self.main_widget)

        # Подключение обработчиков событий
        self.browse_button.triggered.connect(self.browse_file)
        self.edit_video_button.triggered.connect(self.edit_video)
        self.edit_file_size_button.triggered.connect(self.edit_size)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.file_path_edit.setText(file_path)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Все файлы (*.*)")

        if file_path:
            self.file_path_edit.setText(file_path)

    def edit_video(self):
        file_path = self.file_path_edit.text()
        duration = int(self.video_duration_edit.text())

        edit_video_duration(file_path, duration)

        # Отображение Hex-значения
        hex_value = " ".join(f"{b:02X}" for b in duration.to_bytes(8, 'big'))
        self.result_window.setPlainText(hex_value)

    def edit_size(self):
        file_path = self.file_path_edit.text()
        size = int(self.file_size_edit.text())
        unit = self.file_size_unit_combobox.currentText().lower()

        if unit == 'байты':
            new_size = size
        elif unit == 'килобайты':
            new_size = size * 1024
        elif unit == 'мегабайты':
            new_size = size * 1024 * 1024
        elif unit == 'гигабайты':
            new_size = size * 1024 * 1024 * 1024
        elif unit == 'терабайты':
            new_size = size * 1024 * 1024 * 1024 * 1024

        file_type = get_file_type(file_path)
        if file_type == "txt":
            result = edit_file_size(file_path, new_size)
        elif file_type == "mp4":
            result = edit_video_duration(file_path, new_size)
        elif file_type == "png":
            result = edit_image_size(file_path, (new_size, new_size))
        else:
            result = "Не удалось определить тип файла или метод изменения размера не поддерживается."

        self.result_window.setPlainText(result)


def edit_video_duration(file_path, new_duration):
    # Реализация функции изменения длины видео
    pass


def edit_file_size(file_path, new_size):
    # Реализация функции изменения размера файла
    pass


def edit_image_size(file_path, new_size):
    # Реализация функции изменения размера изображения
    pass


def get_file_type(file_path):
    # Реализация функции определения типа файла
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
