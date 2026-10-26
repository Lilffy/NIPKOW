#include "main.h"
#include "stm32f4xx_hal.h"
#include "stm32f4xx_hal_gpio.h"
#include <stdint.h>
static uint8_t ir_on_edge_isr(void){
    static uint8_t stable=1U;
    static uint32_t last=1U;
    static uint32_t t_edge=0U;
    uint32_t raw;
    uint32_t now;
    raw=(HAL_GPIO_ReadPin(IR_INDEX_GPIO_Port,IR_INDEX_Pin)==GPIO_PIN_RESET)? 0U:1U;
    now=HAL_GetTick();
    if(raw!=last){
        last=raw;
        t_edge=now;
    }
    else if((raw!=stable)&&(uint32_t)(now-t_edge)>=20){
        stable=raw;
        if(stable==0U){return 1U;}
    }
    return 0U;}