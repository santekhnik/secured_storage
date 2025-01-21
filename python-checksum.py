def calculate_checksum(data):
    """
    Обчислення контрольної суми (BCC) для заданого масиву байтів.
    
    :param data: список байтів (цілих чисел від 0 до 255)
    :return: контрольна сума (BCC)
    """
    bcc = 0x00  # Початкове значення BCC
    print(f"Initial BCC: 0x{bcc:02X}")

    for i, byte in enumerate(data):
        print(f"Data[{i}]: 0x{byte:02X}, BCC before XOR: 0x{bcc:02X}")
        bcc ^= byte  # Виконання операції XOR
        print(f"BCC after XOR: 0x{bcc:02X}")
    
    return bcc


if __name__ == "__main__":
    # Дані для обчислення контрольної суми
    data = [0x11, 0x36, 0x56, 0x78, 0x9A]  # Змініть значення для тестування

    # Виведення початкового масиву даних
    print("Data array:", " ".join(f"0x{byte:02X}" for byte in data))

    # Обчислення контрольної суми
    checksum = calculate_checksum(data)

    # Виведення результату
    print(f"Final checksum (BCC): 0x{checksum:02X}")
