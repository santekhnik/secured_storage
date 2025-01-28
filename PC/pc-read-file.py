import os
import serial  # Для роботи з UART
import time


def read_data_from_stm(serial_port, baud_rate, chunk_size, timeout=1):
    """
    Читає дані з STM-пристрою через UART.

    :param serial_port: Назва серійного порту (наприклад, "COM3" або "/dev/ttyUSB0")
    :param baud_rate: Швидкість передачі даних (наприклад, 9600, 115200)
    :param chunk_size: Розмір чанку даних для зчитування (в байтах)
    :param timeout: Таймаут для читання (в секундах)
    :return: Список чанків даних (list[bytes])
    """
    chunks = []
    try:
        with serial.Serial(serial_port, baud_rate, timeout=timeout) as ser:
            print(f"Підключено до STM на {serial_port} зі швидкістю {baud_rate} бод.")
            
            while True:
                data = ser.read(chunk_size)  # Читання даних заданого розміру
                if data:  # Якщо отримані дані
                    chunks.append(data)
                    print(f"Отримано чанк: {data}")
                else:
                    print("Немає нових даних. Зупинка читання.")
                    break
    except serial.SerialException as e:
        print(f"Помилка роботи з портом: {e}")
    except Exception as e:
        print(f"Невідома помилка: {e}")
    return chunks


def save_file_from_chunks(chunks, output_file_path):
    """
    Приймає список чанків (частин) даних і зберігає їх у вигляді файлу.

    :param chunks: Список чанків даних (list[bytes])
    :param output_file_path: Шлях до файлу, який потрібно створити (str)
    """
    try:
        with open(output_file_path, 'wb') as output_file:
            for chunk in chunks:
                output_file.write(chunk)
        print(f"Файл успішно відновлено: {output_file_path}")
    except Exception as e:
        print(f"Помилка при відновленні файлу: {e}")


def identify_file_type(file_path):
    """
    Ідентифікує тип файлу за його розширенням.

    :param file_path: Шлях до файлу (str)
    :return: Тип файлу (str)
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    if file_extension in ['.txt']:
        return "text"
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return "image"
    elif file_extension in ['.mp4', '.mkv', '.avi']:
        return "video"
    elif file_extension in ['.pdf', '.docx']:
        return "document"
    else:
        return "unknown"


def process_chunks(chunks, output_file_path):
    """
    Зберігає файл із чанків і додає обробку в залежності від типу файлу.

    :param chunks: Список чанків даних (list[bytes])
    :param output_file_path: Шлях до файлу, який потрібно створити (str)
    """
    save_file_from_chunks(chunks, output_file_path)

    file_type = identify_file_type(output_file_path)

    if file_type == "text":
        print("Файл є текстовим. Можна відкрити в текстовому редакторі.")
    elif file_type == "image":
        print("Файл є зображенням. Можна переглянути в графічному редакторі.")
    elif file_type == "video":
        print("Файл є відео. Можна відтворити в медіаплеєрі.")
    elif file_type == "document":
        print("Файл є документом. Відкрийте його в відповідному додатку.")
    else:
        print("Невідомий тип файлу. Використовуйте універсальний переглядач.")


if __name__ == "__main__":
    # Налаштування порту STM
    serial_port = "COM3"  # Або "/dev/ttyUSB0" для Linux
    baud_rate = 115200
    chunk_size = 64  # Наприклад, 64 байти

    # Читання даних із STM
    chunks = read_data_from_stm(serial_port, baud_rate, chunk_size)

    if chunks:
        output_file_path = "output_from_stm.txt"

        # Обробка і збереження файлу
        process_chunks(chunks, output_file_path)
    else:
        print("Не вдалося отримати дані від STM.")
