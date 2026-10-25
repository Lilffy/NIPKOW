#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

#include "stm32f4xx_hal.h"

/* 固件版本 */
#define FW_VERSION_MAJOR 0
#define FW_VERSION_MINOR 1
#define FW_VERSION_STR   "M0-v0.1"

/* 板级定义（与原理图一致） */
#define LED_PIN          GPIO_PIN_2      /* PB2 用户 LED，低电平点亮 */
#define LED_PORT         GPIOB
#define LED_ON()         HAL_GPIO_WritePin(LED_PORT, LED_PIN, GPIO_PIN_SET)   /* PB2 高电平点亮 */
#define LED_OFF()        HAL_GPIO_WritePin(LED_PORT, LED_PIN, GPIO_PIN_RESET)
#define LED_TOGGLE()     HAL_GPIO_TogglePin(LED_PORT, LED_PIN)

#define IR_PIN           GPIO_PIN_1      /* PA1 红外索引输入 */
#define IR_PORT          GPIOA
#define IR_ACTIVE()      (HAL_GPIO_ReadPin(IR_PORT, IR_PIN) == GPIO_PIN_RESET)

void Error_Handler(void);

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
