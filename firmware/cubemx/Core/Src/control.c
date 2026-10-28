#include "control.h"
#include "rgb.h"
#include "motor.h"

static uint8_t s_target = CONTROL_TARGET_R;
static uint8_t s_level_rgb[3] = {0U, 0U, 0U};
static uint8_t s_level_motor = 0U;

void control_init(void)
{
    s_target = CONTROL_TARGET_R;
    s_level_rgb[0] = 0U;
    s_level_rgb[1] = 0U;
    s_level_rgb[2] = 0U;
    s_level_motor = 0U;
}

uint8_t control_target(void)
{
    return s_target;
}

void control_set_target(uint8_t target)
{
    if (target <= CONTROL_TARGET_M) {
        s_target = target;
    }
}

void control_next_target(void)
{
    s_target = (uint8_t)((s_target + 1U) % 4U);
}

void control_level_step(void)
{
    if (s_target == CONTROL_TARGET_M) {
        s_level_motor = (uint8_t)((s_level_motor + 1U) % CONTROL_LEVEL_COUNT);
    } else {
        s_level_rgb[s_target] = (uint8_t)((s_level_rgb[s_target] + 1U) % CONTROL_LEVEL_COUNT);
    }
}

uint8_t control_level(void)
{
    return (s_target == CONTROL_TARGET_M) ? s_level_motor : s_level_rgb[s_target];
}

uint8_t control_level_of(uint8_t target)
{
    if (target == CONTROL_TARGET_M) {
        return s_level_motor;
    }
    return (target <= 2U) ? s_level_rgb[target] : 0U;
}

bool control_set_level(uint8_t target, uint8_t level)
{
    if (level >= CONTROL_LEVEL_COUNT) {
        return false;
    }
    if (target == CONTROL_TARGET_M) {
        s_level_motor = level;
    } else if (target <= 2U) {
        s_level_rgb[target] = level;
    } else {
        return false;
    }
    return true;
}

void control_apply(void)
{
    if (s_target == CONTROL_TARGET_M) {
        motor_set(CONTROL_TARGET_M, s_level_motor);
    } else {
        rgb_set(s_target, s_level_rgb[s_target]);
        rgb_use();
    }
}
