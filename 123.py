import os
import ctypes
import winreg
from tkinter import *


def delete_autorun_file(drive_letter):
    autorun_file = os.path.join(drive_letter, "autorun.inf")

    try:
        os.remove(autorun_file)
        print(f"Файл {autorun_file} удален.")
    except OSError as e:
        print(f"Не удалось удалить файл {autorun_file}: {e}")


def disable_usb_autorun():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, "NoDriveTypeAutoRun", 0, winreg.REG_DWORD, 0xFF)
        winreg.CloseKey(reg_key)

        print("Автозапуск для USB-устройств отключен.")
    except Exception as e:
        print(f"Ошибка при отключении автозапуска для USB-устройств: {e}")


def enable_autorun_reading():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, "NoDriveTypeAutoRun", 0, winreg.REG_DWORD, 0x0)
        winreg.CloseKey(reg_key)

        print("Автозапуск для autorun файла включен.")
    except Exception as e:
        print(f"Ошибка при включении автозапуска для autorun файла: {e}")


root = Tk()
root.title("Управление автозапуском")
root.geometry("300x200")

# Метка для вывода сообщений
label = Label(root, text="")
label.pack(pady=10)

# Кнопка "Отключить автозапуск"
btn_disable_autorun = Button(root, text="Отключить автозапуск", command=disable_usb_autorun)
btn_disable_autorun.pack(pady=5)

# Кнопка "Включить чтение autorun файла"
btn_enable_autorun_reading = Button(root, text="Включить чтение autorun файла", command=enable_autorun_reading)
btn_enable_autorun_reading.pack(pady=5)

# Запуск главного цикла Tkinter
root.mainloop()
