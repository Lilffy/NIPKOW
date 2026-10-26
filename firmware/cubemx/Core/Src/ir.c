
#include "ir.h"
#include "main.h"

static volatile uint32_t g_last_ms = 0U;
static volatile uint32_t g_count   = 0U;
static volatile bool     g_event   = false;

void ir_init(void)
{
    
    g_last_ms = HAL_GetTick();
}

void ir_on_edge_isr(void)
{
    uint32_t now = HAL_GetTick();
    if ((uint32_t)(now - g_last_ms) < IR_DEBOUNCE_MS)
        return;                     
    g_last_ms = now;
    g_count++;
    g_event = true;
}

uint32_t ir_count(void)        { return g_count; }
uint32_t ir_last_edge_ms(void) { return g_last_ms; }

bool ir_take_event(void)
{
    if (!g_event) return false;
    g_event = false;
    return true;
}