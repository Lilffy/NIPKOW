#include "main.h"

/* SysTick 中断：HAL 时基 */
void SysTick_Handler(void)
{
    HAL_IncTick();
}

/* PA1 红外索引（M1 启用 EXTI） */
void EXTI1_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(IR_PIN);
}

/* 供 M1 使用的中断回调（当前空实现） */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    (void)GPIO_Pin;
}
