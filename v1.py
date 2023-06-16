import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QPlainTextEdit, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PIL import Image


# Функция для изменения длины видео
def edit_video_duration(file_path, new_duration):
    try:
        with open(file_path, 'r+b') as f:
            f.seek(0)  # Перемещаемся в начало файла
            data = f.read()

            # Находим позицию для изменения длины видео
            start_position = data.find(b'mvhd') + 15

            # Конвертируем десятичное значение в шестнадцатеричный формат
            duration_hex = ' '.join(f'{int(new_duration):02X}' for new_duration in new_duration.to_bytes(8, 'big'))

            duration_bytes = bytes.fromhex(duration_hex)

            # Заменяем значение длины видео в hex-коде
            data = data[:start_position] + duration_bytes + data[start_position + 6:]

            # Записываем измененные данные обратно в файл
            f.seek(0)
            f.write(data)

        print("Изменения успешно сохранены.")
        print(f"Новая продолжительность видео: {new_duration} секунд")
    except Exception as e:
        print(f"Произошла ошибка при редактировании видео: {str(e)}")

# Функция для изменения размера файла
def edit_file_size(file_path, new_size):
    try:
        with open(file_path, 'r+b') as f:
            f.seek(0, os.SEEK_END)  # Перемещаемся в конец файла
            current_size = f.tell()

            if new_size > current_size:
                # Увеличиваем размер файла путем добавления нулевых байтов
                f.write(b'\x00' * (new_size - current_size))
            elif new_size < current_size:
                # Уменьшаем размер файла путем обрезки содержимого
                f.seek(new_size)
                f.truncate()

        size_info = f"Размер файла успешно изменен.\nНовый размер: {new_size} байт"
        return size_info

    except Exception as e:
        error_message = f"Произошла ошибка при изменении размера файла: {str(e)}"
        return error_message


# Функция для изменения размера изображения
def edit_image_size(file_path, new_size):
    try:
        image = Image.open(file_path)
        image = image.resize(new_size)
        image.save(file_path)
        return f"Размер изображения успешно изменен."
    except Exception as e:
        return f"Произошла ошибка при изменении размера изображения: {str(e)}"

# Функция для определения типа файла
def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return "txt"
    elif ext == ".mp4":
        return "mp4"
    elif ext == ".png":
        return "png"
    else:
        return None


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
        self.browse_button = QPushButton("Обзор")

        self.video_duration_label = QLabel("Введите новую продолжительность (в секундах):")
        self.video_duration_edit = QLineEdit()
        self.edit_video_button = QPushButton("Редактировать видео")

        self.file_size_label = QLabel("Изменить размер файла:")
        self.file_size_edit = QLineEdit()
        self.file_size_unit_combobox = QComboBox()
        self.file_size_unit_combobox.addItems(['байты', 'килобайты', 'мегабайты', 'гигабайты', 'терабайты'])
        self.edit_file_size_button = QPushButton("Редактировать размер файла")

        self.result_label = QLabel("Результат:")
        self.result_window = QPlainTextEdit()
        self.result_window.setReadOnly(True)

        # Размещение компонентов на главном виджете
        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_path_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.video_duration_label)
        layout.addWidget(self.video_duration_edit)
        layout.addWidget(self.edit_video_button)
        layout.addWidget(self.file_size_label)
        layout.addWidget(self.file_size_edit)
        layout.addWidget(self.file_size_unit_combobox)
        layout.addWidget(self.edit_file_size_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_window)
        self.main_widget.setLayout(layout)

        # Установка главного виджета
        self.setCentralWidget(self.main_widget)

        # Подключение обработчиков событий
        self.browse_button.clicked.connect(self.browse_file)
        self.edit_video_button.clicked.connect(self.edit_video)
        self.edit_file_size_button.clicked.connect(self.edit_size)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())