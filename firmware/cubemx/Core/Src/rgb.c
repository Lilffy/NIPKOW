
#include "rgb.h"
#include "main.h"
#include <stdint.h>

extern TIM_HandleTypeDef htim3;

/* 三路实际占空比 0..1000（0=灭，1000=最亮），由 rgb_use() 统一反相输出 */
volatile uint16_t rgb[3] = {0U, 0U, 0U};
static const uint16_t brightness_level_table[6] = {0U, 200U, 400U, 600U, 800U, 1000U};
#define PWM_PERIOD 1000U

void rgb_set(uint8_t target, uint16_t level)
{
    if ((target > 2U) || (level >= 6U)) {
        return;
    }
    rgb[target] = brightness_level_table[level];
}

/* PNP 高边：占空比越大越亮，CCR 取反 */
void rgb_use(void)
{
    uint16_t r = rgb[0];
    uint16_t g = rgb[1];
    uint16_t b = rgb[2];

    if (r > PWM_PERIOD) r = PWM_PERIOD;
    if (g > PWM_PERIOD) g = PWM_PERIOD;
    if (b > PWM_PERIOD) b = PWM_PERIOD;

    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, PWM_PERIOD - r);
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, PWM_PERIOD - g);
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_3, PWM_PERIOD - b);
}

void rgb_init(void)
{
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_3);

    rgb[0] = 0U;
    rgb[1] = 0U;
    rgb[2] = 0U;
    rgb_use();                      /* 上电全灭 */
}
