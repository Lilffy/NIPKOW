
#include "ir.h"
#include "main.h"     /* 为了 HAL_GetTick / HAL_GPIO_EXTI_Callback */

static volatile uint32_t g_count      = 0;
static volatile uint32_t g_last_ms    = 0;
static volatile bool     g_event      = false;

void ir_init(void)
{
    /* TODO: 确保 PA1 EXTI 已由 CubeMX 配好；
     *      如果 NVIC 还没开，在这里 HAL_NVIC_EnableIRQ(EXTI1_IRQn)。 */
}

void ir_on_edge_isr(void)
{
    /* TODO: 1) now = HAL_GetTick();
     *       2) if (now - g_last_ms < IR_DEBOUNCE_MS) return;  // 抖动
     *       3) g_last_ms = now; g_count++; g_event = true; */
}

uint32_t ir_count(void)        { return g_count; }
uint32_t ir_last_edge_ms(void) { return g_last_ms; }

bool ir_take_event(void)
{
    /* TODO: 取走即清（注意：两个边沿挨得近时可能丢一个事件，考虑用计数差分） */
    if (g_event) { g_event = false; return true; }
    return false;
}