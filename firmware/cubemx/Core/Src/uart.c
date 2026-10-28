#include "uart.h"
#include "main.h"
#include <string.h>

extern UART_HandleTypeDef huart2;

#define RX_RING_SIZE   256U
#define LINE_MAX_LEN   96U

static volatile uint8_t  s_rx_ring[RX_RING_SIZE];
static volatile uint16_t s_rx_head = 0U;
static volatile uint16_t s_rx_tail = 0U;
static uint8_t s_rx_byte = 0U;

static void uart_push(uint8_t b)
{
    uint16_t next = (uint16_t)((s_rx_head + 1U) % RX_RING_SIZE);
    if (next != s_rx_tail) {
        s_rx_ring[s_rx_head] = b;
        s_rx_head = next;
    }
}

static int uart_pop(void)
{
    if (s_rx_head == s_rx_tail) {
        return -1;
    }
    uint8_t b = s_rx_ring[s_rx_tail];
    s_rx_tail = (uint16_t)((s_rx_tail + 1U) % RX_RING_SIZE);
    return (int)b;
}

void uart_init(void)
{
    s_rx_head = 0U;
    s_rx_tail = 0U;

    /* CubeMX 里 USART2 全局中断未在生成代码中使能，这里补上 */
    HAL_NVIC_SetPriority(USART2_IRQn, 5U, 0U);
    HAL_NVIC_EnableIRQ(USART2_IRQn);

    (void)HAL_UART_Receive_IT(&huart2, &s_rx_byte, 1U);
}

/* 取一整行（\n 结尾，去掉 \r），非阻塞；没有完整行返回 false */
bool uart_get_line(char *out, uint16_t maxlen)
{
    static char     line[LINE_MAX_LEN];
    static uint16_t len = 0U;
    int c;

    if ((out == NULL) || (maxlen < 2U)) {
        return false;
    }

    while ((c = uart_pop()) >= 0) {
        if (c == '\r') {
            continue;
        }
        if (c == '\n') {
            if (len > 0U) {
                line[len] = '\0';
                (void)strncpy(out, line, (size_t)(maxlen - 1U));
                out[maxlen - 1U] = '\0';
                len = 0U;
                return true;
            }
            len = 0U;
            continue;
        }
        if (len < (uint16_t)(sizeof(line) - 1U)) {
            line[len++] = (char)c;
        } else {
            len = 0U;   /* 超长丢弃 */
        }
    }
    return false;
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART2) {
        uart_push(s_rx_byte);
        (void)HAL_UART_Receive_IT(&huart2, &s_rx_byte, 1U);
    }
}

void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART2) {
        __HAL_UART_CLEAR_OREFLAG(huart);
        (void)HAL_UART_Receive_IT(&huart2, &s_rx_byte, 1U);
    }
}
