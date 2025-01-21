/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f0xx_hal.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

/* Private variables ---------------------------------------------------------*/
UART_HandleTypeDef huart1;

uint8_t rx_data[1];          // Буфер для прийому одного байта
uint8_t rx_buffer[255];      // Буфер для зберігання прийнятих команд
uint8_t rand_buffer[255];
uint8_t rx_index = 0;        // Поточний індекс для запису в rx_buffer
uint32_t *hexCode[9]; // Глобальна змінна для зберігання коду у 32-ковому форматі

#define FLASH_USER_START_ADDR   ((uint32_t)0x08008000) // Початкова адреса флеш-пам'яті
#define FLASH_USER_END_ADDR     ((uint32_t)0x08010000) // Кінцева адреса флеш-пам'яті
#define MAX_PACKET_SIZE         128                     // Розмір одного пакета даних

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART1_UART_Init(void);

/* USER CODE BEGIN 0 */
// Функція для запису у флеш-пам'ять
void Flash_Write(uint32_t startAddress, uint8_t *data, uint16_t length) {
    HAL_FLASH_Unlock();
    for (uint16_t i = 0; i < length; i++) {
        HAL_FLASH_Program(FLASH_TYPEPROGRAM_HALFWORD, startAddress + i * 2, data[i]);
    }
    HAL_FLASH_Lock();
}

// Функція для читання з флеш-пам'яті
void Flash_Read(uint32_t startAddress, uint8_t *data, uint16_t length) {
    for (uint16_t i = 0; i < length; i++) {
        data[i] = *(__IO uint8_t *)(startAddress + i);
    }
}

void Flash_Erase(uint32_t startAddress, uint32_t endAddress) {
    HAL_FLASH_Unlock();

    FLASH_EraseInitTypeDef eraseInitStruct;
    uint32_t pageError = 0;

    eraseInitStruct.TypeErase = FLASH_TYPEERASE_PAGES;
    eraseInitStruct.PageAddress = startAddress;
    eraseInitStruct.NbPages = (endAddress - startAddress) / FLASH_PAGE_SIZE;

    if (HAL_FLASHEx_Erase(&eraseInitStruct, &pageError) != HAL_OK) {
        HAL_UART_Transmit(&huart1, (uint8_t *)"Flash erase failed!\n\r", 22, HAL_MAX_DELAY);
        Error_Handler();
    }

    HAL_FLASH_Lock();
}

//// Чекаємо отримання команди через UART
//            if (HAL_UART_Receive(&huart1, (uint8_t *)buffer, sizeof(buffer), HAL_MAX_DELAY) == HAL_OK) {
//                if (strncmp(buffer, "GEN_CODE", 8) == 0) { // Якщо команда "GEN_CODE"
//                    generate_random_code(random_code); // Генеруємо 32-бітний код
//                    HAL_UART_Transmit(&huart1, (uint8_t *)random_code, strlen(random_code), HAL_MAX_DELAY); // Відправляємо назад
//                }
//            }


void generate_random_code() {
    uint32_t random_value = rand(); // Генеруємо 32-бітне випадкове число і символи
    sprintf(hexCode, "%08X", random_value); // Конвертуємо у 16-ковий формат
}

// --------------(НАРАЗІ НА ПАУЗІ)-------Функція для генерації випадкового пароля
//void generate_password(char *password, int length) {
//    const char charset[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
//                           "abcdefghijklmnopqrstuvwxyz"
//                           "0123456789"
//                           "!@#$%^&*()";
//    size_t charset_size = strlen(charset);
//
//    for (int i = 0; i < length; i++) {
//        password[i] = charset[rand() % charset_size];
//    }
//    password[length] = '\0'; // Завершальний символ
//}


void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart->Instance == USART1) {
        if (rx_data[0] == '\r') {
            rx_buffer[rx_index] = '\0';
            rx_index = 0;

            if (strncmp((char *)rx_buffer, "WRITE_FLASH", 11) == 0) {
                uint8_t *data = (uint8_t *)(rx_buffer + 12);
                uint16_t data_length = strlen((char *)data);

                // Очищення флеш-пам'яті
                Flash_Erase(FLASH_USER_START_ADDR, FLASH_USER_END_ADDR);

                // Запис даних у флеш
                Flash_Write(FLASH_USER_START_ADDR, data, data_length);
                HAL_UART_Transmit(&huart1, (uint8_t *)"Data written to flash\n\r", 24, HAL_MAX_DELAY);
            } else if (strncmp((char *)rx_buffer, "RAND_PASS", 9) == 0) {
            	generate_random_code(); // Генеруємо 32-бітний код
                HAL_UART_Transmit(&huart1, hexCode, 8, HAL_MAX_DELAY);
            } else if (strcmp((char *)rx_buffer, "READ_FLASH") == 0) {
                uint8_t packet[MAX_PACKET_SIZE];
                uint32_t address = FLASH_USER_START_ADDR;

                while (address < FLASH_USER_END_ADDR) {
                    Flash_Read(address, packet, sizeof(packet));
                    HAL_UART_Transmit(&huart1, packet, sizeof(packet), HAL_MAX_DELAY);
                    address += sizeof(packet);
                }

                HAL_UART_Transmit(&huart1, (uint8_t *)"Flash read complete\n\r", 22, HAL_MAX_DELAY);
            } else {
                HAL_UART_Transmit(&huart1, (uint8_t *)"Unknown command\n\r", 17, HAL_MAX_DELAY);
            }
        } else {
            rx_buffer[rx_index++] = rx_data[0];
        }

        HAL_UART_Receive_IT(&huart1, rx_data, 1);
    }
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void) {
    HAL_Init();               // Ініціалізація HAL
    SystemClock_Config();     // Налаштування системного годинника
    MX_GPIO_Init();           // Ініціалізація GPIO
    MX_USART1_UART_Init();    // Ініціалізація UART

    // Зразок для тестування: записати рядок у флеш-пам'ять
    uint8_t data_to_store[256] = "Hello, this is test data for flash memory!";
    Flash_Write(FLASH_USER_START_ADDR, data_to_store, strlen((char *)data_to_store));

    // Увімкнути переривання для прийому UART
    HAL_UART_Receive_IT(&huart1, rx_data, 1);

    while (1) {



        }
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void) {
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    /** Налаштування осцилятора */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;  // Видаліть цей рядок для STM32F0
    RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL12;
    RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1;

    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
        Error_Handler();
    }

    /** Налаштування шин */
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_PCLK1;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK) {
        Error_Handler();
    }
}


/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void) {
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 38400;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart1.Init.OverSampling = UART_OVERSAMPLING_16;
    if (HAL_UART_Init(&huart1) != HAL_OK) {
        Error_Handler();
    }
}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void) {
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();
}

/**
  * @brief Error Handler
  * @retval None
  */
void Error_Handler(void) {
    __disable_irq();
    while (1) {
    }
}
