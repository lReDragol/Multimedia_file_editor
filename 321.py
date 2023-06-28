import time
import psutil
import win32api
import win32file


def get_usb_drives():
    drives = []
    drive_bitmask = win32api.GetLogicalDrives()
    for letter in range(65, 91):
        mask = 1 << (letter - 65)
        if drive_bitmask & mask:
            drives.append(chr(letter) + ":\\")
    return drives


def monitor_usb():
    previous_drives = []
    while True:
        drives = get_usb_drives()
        new_drives = list(set(drives) - set(previous_drives))
        if new_drives:
            for drive in new_drives:
                try:
                    drive_info = win32api.GetVolumeInformation(drive)
                    drive_label = drive_info[0] if len(drive_info) > 0 else "Н/Д"
                    drive_serial = drive_info[1] if len(drive_info) > 1 else "Н/Д"
                    drive_filesystem = drive_info[4] if len(drive_info) > 4 else "Н/Д"
                    drive_size = psutil.disk_usage(drive).total / (1024 ** 3)
                    drive_free = psutil.disk_usage(drive).free / (1024 ** 3)
                    drive_used = psutil.disk_usage(drive).used / (1024 ** 3)
                    drive_percent = psutil.disk_usage(drive).percent
                    volume_path = win32file.GetVolumePathName(drive)
                    computer_name = win32api.GetComputerName()
                    print("------------------------------")
                    print("Подключен USB-накопитель:")
                    print("Буква диска:", drive)
                    print("Метка диска:", drive_label)
                    print("Серийный номер диска:", drive_serial)
                    print("Файловая система:", drive_filesystem)
                    print("Размер диска:", drive_size, "ГБ")
                    print("Свободное пространство:", drive_free, "ГБ")
                    print("Используемое пространство:", drive_used, "ГБ")
                    print("Процент использования:", drive_percent, "%")
                    print("Точка монтирования:", volume_path)
                    print("Имя компьютера, на котором смонтирован диск:", computer_name)

                    print("Список файлов на диске:")
                    for file in psutil.disk_partitions():
                        if file.device == drive:
                            print("- ", file.mountpoint)

                    if len(drive_info) > 2:
                        print("Метка тома:", drive_info[2])
                    if len(drive_info) > 3:
                        print("Системный том:", drive_info[3])
                    if len(drive_info) > 5:
                        print("Серийный номер файловой системы:", drive_info[5])
                    if len(drive_info) > 6:
                        print("Максимальная длина имени файла:", drive_info[6])
                    if len(drive_info) > 7:
                        print("Тип файловой системы:", drive_info[7])
                    if len(drive_info) > 8:
                        print("Количество секторов:", drive_info[8])
                    if len(drive_info) > 9:
                        print("Количество свободных секторов:", drive_info[9])
                    if len(drive_info) > 10:
                        print("Общий размер сектора (в байтах):", drive_info[10])
                    if len(drive_info) > 11:
                        print("Метка тома (Unicode):", drive_info[11])
                    if len(drive_info) > 12:
                        print("Файловая система (Unicode):", drive_info[12])
                        print("------------------------------")

                except Exception as e:
                    print(f"Ошибка при получении информации о диске {drive}: {str(e)}")
                    print("------------------------------")

        previous_drives = drives
        time.sleep(1)


if __name__ == "__main__":
    monitor_usb()
