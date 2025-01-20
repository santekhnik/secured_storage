import serial

ser = serial.Serial('COM4', 38400, timeout=1)  # Змініть COM4 на свій порт

def write_flash(data):

    command = f"WRITE_FLASH {data}\r"
    ser.write(command.encode())
    response = ser.readline().decode().strip()
    print(f"STM32 відповів: {response}")

def read_flash():
    """
    Запитує дані з флеш-пам'яті STM32.
    """
    ser.write("READ_FLASH\r".encode())
    print("Отримання даних з флеш-пам'яті...")

    result = ""
    while True:
        packet = ser.read(64)
        if not packet:
            break
        result += packet.decode(errors='ignore')

    print(f"Отримані дані: {result.strip()}")

def main():
    """
    Основна функція для взаємодії з STM32.
    """
    try:
        while True:
            print("\nМеню:")
            print("1. Записати дані у флеш (WRITE_FLASH)")
            print("2. Прочитати дані з флеш (READ_FLASH)")
            print("3. Вийти")
            choice = input("Ваш вибір: ")

            if choice == "1":
                data = input("Введіть дані для запису: ")
                write_flash(data)
            elif choice == "2":
                read_flash()
            elif choice == "3":
                print("Програма завершена.")
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")
    except KeyboardInterrupt:
        print("\nПрограма зупинена.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
