
#include "key.h"
#include "main.h"

#define KEY_DEBOUNCE_MS 20U

/* 每个按键独立的去抖状态 + 计数 */
typedef struct {
    uint8_t  stable;
    uint8_t  last;
    uint32_t t_edge;
    uint32_t cnt;
} key_state_t;

static key_state_t g_keys[2] = {
    {1U, 1U, 0U, 0U},   /* KEY1: PC0 */
    {1U, 1U, 0U, 0U},   /* KEY2: PC1 */
};

static void key_scan(uint8_t idx)
{
    key_state_t *k = &g_keys[idx];
    uint8_t  raw;
    uint32_t now;

    raw = (idx == 0U)
        ? ((HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_RESET) ? 0U : 1U)
        : ((HAL_GPIO_ReadPin(KEY2_GPIO_Port, KEY2_Pin) == GPIO_PIN_RESET) ? 0U : 1U);
    now = HAL_GetTick();

    if (raw != k->last) {
        k->last = raw;
        k->t_edge = now;
    } else if ((raw != k->stable) && ((uint32_t)(now - k->t_edge) >= KEY_DEBOUNCE_MS)) {
        k->stable = raw;
        if (k->stable == 0U) {
            k->cnt++;               /* 下降沿 = 按下 */
        }
    }
}

void key1_press(void) { key_scan(0U); }
void key2_press(void) { key_scan(1U); }

uint32_t key1_cnt(void) { return g_keys[0].cnt; }
uint32_t key2_cnt(void) { return g_keys[1].cnt; }
