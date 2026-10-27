
#include "motor.h"
#include "main.h"
#include <stdint.h>

extern TIM_HandleTypeDef htim4;

/*
 * TIM4: PSC=167, ARR=999 -> 1 kHz（当前为占位频率，到货后按电机要求改；
 *       若是电调型 50 Hz / 1-2 ms 脉宽，改 PSC/ARR 与下面映射）
 * 表里是 CCR 值（0..1000），不是百分比。
 */
static const uint16_t motor_level_table[MOTOR_LEVEL_COUNT] = {
    0U, 200U, 400U, 600U, 800U, 1000U
};

void motor_set(uint8_t target, uint16_t level)
{
    if ((target != 3U) || (level >= MOTOR_LEVEL_COUNT)) {
        return;
    }
    __HAL_TIM_SET_COMPARE(&htim4, TIM_CHANNEL_1, motor_level_table[level]);
}

void motor_init(void)
{
    HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_1);
    __HAL_TIM_SET_COMPARE(&htim4, TIM_CHANNEL_1, 0U);   /* 上电停转 */
}
