/* M0 骨架：168 MHz、USART2 115200、PB2 心跳灯
 * 板：立创·天空星 STM32F407VET6（8 MHz 外部晶振）
 */
#include "main.h"
#include <stdio.h>
#include <string.h>

UART_HandleTypeDef huart2;

static void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);

/* printf 重定向到 USART2 */
int _write(int file, char *ptr, int len)
{
    (void)file;
    HAL_UART_Transmit(&huart2, (uint8_t *)ptr, (uint16_t)len, HAL_MAX_DELAY);
    return len;
}

int main(void)
{
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_USART2_UART_Init();

    printf("\r\n=== NIPKOW %s ===\r\n", FW_VERSION_STR);
    printf("SYSCLK = %lu Hz\r\n", (unsigned long)HAL_RCC_GetSysClockFreq());
    printf("HCLK   = %lu Hz\r\n", (unsigned long)HAL_RCC_GetHCLKFreq());
    printf("PCLK1  = %lu Hz\r\n", (unsigned long)HAL_RCC_GetPCLK1Freq());
    printf("PCLK2  = %lu Hz\r\n", (unsigned long)HAL_RCC_GetPCLK2Freq());
    printf("等待 ST-Link / 串口指令...\r\n");

    uint32_t last_beat = HAL_GetTick();
    uint32_t last_msg  = HAL_GetTick();

    while (1)
    {
        uint32_t now = HAL_GetTick();

        /* 500 ms 心跳翻转（1 Hz 闪烁） */
        if (now - last_beat >= 500U)
        {
            last_beat = now;
            LED_TOGGLE();
        }

        /* 1 s 打印一次 */
        if (now - last_msg >= 1000U)
        {
            last_msg = now;
            printf("[hb] tick=%lu led=%d\r\n", (unsigned long)now,
                   (HAL_GPIO_ReadPin(LED_PORT, LED_PIN) == GPIO_PIN_RESET) ? 1 : 0);
        }
    }
}

static void SystemClock_Config(void)
{
    RCC_OscInitTypeDef osc = {0};
    RCC_ClkInitTypeDef clk = {0};

    __HAL_RCC_PWR_CLK_ENABLE();
    __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

    /* HSE 8 MHz -> PLL: M=8, N=336, P=2 -> 168 MHz; Q=7 -> 48 MHz */
    osc.OscillatorType      = RCC_OSCILLATORTYPE_HSE;
    osc.HSEState            = RCC_HSE_ON;
    osc.PLL.PLLState        = RCC_PLL_ON;
    osc.PLL.PLLSource       = RCC_PLLSOURCE_HSE;
    osc.PLL.PLLM            = 8;
    osc.PLL.PLLN            = 336;
    osc.PLL.PLLP            = RCC_PLLP_DIV2;
    osc.PLL.PLLQ            = 7;
    if (HAL_RCC_OscConfig(&osc) != HAL_OK)
    {
        Error_Handler();
    }

    clk.ClockType      = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK |
                         RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
    clk.SYSCLKSource   = RCC_SYSCLKSOURCE_PLLCLK;
    clk.AHBCLKDivider  = RCC_SYSCLK_DIV1;   /* 168 MHz */
    clk.APB1CLKDivider = RCC_HCLK_DIV4;     /* 42 MHz */
    clk.APB2CLKDivider = RCC_HCLK_DIV2;     /* 84 MHz */
    if (HAL_RCC_ClockConfig(&clk, FLASH_LATENCY_5) != HAL_OK)
    {
        Error_Handler();
    }
}

static void MX_GPIO_Init(void)
{
    GPIO_InitTypeDef g = {0};

    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();

    /* PB2 用户 LED，推挽输出，默认熄灭（高电平） */
    HAL_GPIO_WritePin(LED_PORT, LED_PIN, GPIO_PIN_SET);
    g.Pin   = LED_PIN;
    g.Mode  = GPIO_MODE_OUTPUT_PP;
    g.Pull  = GPIO_NOPULL;
    g.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(LED_PORT, &g);

    /* PA1 红外索引输入：上拉，M1 再切 EXTI */
    g.Pin  = IR_PIN;
    g.Mode = GPIO_MODE_INPUT;
    g.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(IR_PORT, &g);
}

static void MX_USART2_UART_Init(void)
{
    GPIO_InitTypeDef g = {0};

    __HAL_RCC_USART2_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    /* PA2 = TX, PA3 = RX, AF7 */
    g.Pin       = GPIO_PIN_2 | GPIO_PIN_3;
    g.Mode      = GPIO_MODE_AF_PP;
    g.Pull      = GPIO_PULLUP;
    g.Speed     = GPIO_SPEED_FREQ_VERY_HIGH;
    g.Alternate = GPIO_AF7_USART2;
    HAL_GPIO_Init(GPIOA, &g);

    huart2.Instance          = USART2;
    huart2.Init.BaudRate     = 115200;
    huart2.Init.WordLength   = UART_WORDLENGTH_8B;
    huart2.Init.StopBits     = UART_STOPBITS_1;
    huart2.Init.Parity       = UART_PARITY_NONE;
    huart2.Init.Mode         = UART_MODE_TX_RX;
    huart2.Init.HwFlowCtl    = UART_HWCONTROL_NONE;
    huart2.Init.OverSampling = UART_OVERSAMPLING_16;
    if (HAL_UART_Init(&huart2) != HAL_OK)
    {
        Error_Handler();
    }
}

void Error_Handler(void)
{
    __disable_irq();
    while (1)
    {
        /* 快闪：错误状态 */
        HAL_GPIO_TogglePin(LED_PORT, LED_PIN);
        for (volatile uint32_t i = 0; i < 200000U; i++) { }
    }
}
