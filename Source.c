#include "main.h"
#include "bcc.h" // Модуль для розрахунку BCC
#include "usart.h" // Драйвер UART

void UART_SendString(char* str) {
    while (*str) {
        HAL_UART_Transmit(&huart1, (uint8_t*)str, 1, HAL_MAX_DELAY);
        str++;
    }
}

void UART_SendHex(uint8_t value) {
    char hexStr[5]; // Формат: "0xXX "
    sprintf(hexStr, "0x%02X ", value);
    UART_SendString(hexStr);
}

void UART_SendNewLine(void) {
    char newline[] = "\r\n";
    HAL_UART_Transmit(&huart1, (uint8_t*)newline, sizeof(newline) - 1, HAL_MAX_DELAY);
}

int main(void) {
    // Ініціалізація HAL та апаратного забезпечення
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_USART1_UART_Init();

    // Дані для розрахунку BCC
    uint8_t data[] = { 0x11, 0x36, 0x56, 0x78, 0x9A }; // Ваші дані
    uint16_t length = sizeof(data) / sizeof(data[0]);

    // Вивід початкового масиву через UART
    UART_SendString("Data array: ");
    for (uint16_t i = 0; i < length; i++) {
        UART_SendHex(data[i]);
    }
    UART_SendNewLine();

    // Розрахунок BCC
    uint8_t bcc = CalculateBCC(data, length);

    // Вивід фінального результату
    UART_SendString("Final BCC: ");
    UART_SendHex(bcc);
    UART_SendNewLine();

    // Основний цикл програми
    while (1) {
    }
}
