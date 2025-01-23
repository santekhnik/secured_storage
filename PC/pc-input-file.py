import serial
import time
import os

# Конфігурація UART
PORT = "COM4"  # Вкажіть ваш COM порт
BAUDRATE = 38400
TIMEOUT = 1

CHUNK_SIZE = 256  # Розмір фрагменту в байтах

ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)

def create_packet(chunk_data, offset):
    """
    Створення пакету з offset і даними.
    """
    header = 0x01  # Заголовок
    footer = 0x03  # Закінчення пакету

    # Формування пакету
    packet = bytearray()
    packet.append(header)  # Додати заголовок
    packet.append(offset & 0xFF)          # Молодший байт offset
    packet.append((offset >> 8) & 0xFF)  # Старший байт offset
    packet.append(len(chunk_data))       # Розмір даних
    packet.extend(chunk_data)            # Дані
    packet.append(footer)                # Додати закінчення пакету

    return packet

def send_file_with_offset(filename):
    if not os.path.exists(filename):
        print(f"Файл {filename} не знайдено!")
        return

    with open(filename, "rb") as f:
        file_data = f.read()

    total_size = len(file_data)
    num_chunks = (total_size + CHUNK_SIZE - 1) // CHUNK_SIZE  # Кількість фрагментів

    print(f"Файл розміром {total_size} байт розбитий на {num_chunks} частин.")

    for chunk_index in range(num_chunks):
        # Визначення offset
        offset = chunk_index * CHUNK_SIZE
        chunk_data = file_data[offset:offset + CHUNK_SIZE]  # Витяг фрагмента даних

        # Створення і надсилання пакету
        packet = create_packet(chunk_data, offset)
        ser.write(packet)
        print(f"Відправлено фрагмент {offset} (розмір: {len(chunk_data)} байт)")

        time.sleep(0.1)  # Невелика затримка між відправленнями

    print("Відправка файлу завершена.")

if __name__ == "__main__":
    try:
        # Вкажіть шлях до вашого файлу
        file_path = r"C:\Робочий стіл\1.txt"
        send_file_with_offset(file_path)
    except KeyboardInterrupt:
        print("Передача перервана користувачем.")
    finally:
        ser.close()