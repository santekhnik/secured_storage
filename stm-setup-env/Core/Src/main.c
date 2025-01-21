#include "stm32f0xx_hal.h"

// Ініціалізація світлодіодів
void MX_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    // Включаємо тактування для портів, де підключені світлодіоди
    __HAL_RCC_GPIOC_CLK_ENABLE();

    // Налаштування пінів для світлодіодів
    GPIO_InitStruct.Pin = GPIO_PIN_9 | GPIO_PIN_8;  // Піни LD4 і LD3
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;     // Режим виходу
    GPIO_InitStruct.Pull = GPIO_NOPULL;             // Без підтягу
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;    // Низька швидкість
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
}

// Основна функція
int main(void)
{
    // Ініціалізація HAL
    HAL_Init();

    // Ініціалізація GPIO
    MX_GPIO_Init();

    // Безкінечний цикл для миготіння світлодіодів
    while (1)
    {
        // Увімкнути світлодіод LD4
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_9, GPIO_PIN_SET);
        // Вимкнути світлодіод LD3
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_8, GPIO_PIN_RESET);

        // Затримка 500 мс
        HAL_Delay(500);

        // Вимкнути світлодіод LD4
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_9, GPIO_PIN_RESET);
        // Увімкнути світлодіод LD3
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_8, GPIO_PIN_SET);

        // Затримка 500 мс
        HAL_Delay(500);
    }
}
