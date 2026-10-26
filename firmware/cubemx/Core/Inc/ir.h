/* Core/Inc/ir.h —— 只有声明，没有实现 */
#ifndef IR_H
#define IR_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* 两次边沿间隔小于该值视为抖动，丢弃 */
#define IR_DEBOUNCE_MS  20U

void     ir_init(void);             /* 初始化（NVIC 由 CubeMX 已使能） */
void     ir_on_edge_isr(void);      /* EXTI 回调里调用：只记时间戳/置标志 */
uint32_t ir_count(void);            /* 累计有效脉冲数 */
uint32_t ir_last_edge_ms(void);     /* 最近一次有效边沿的时间戳(ms) */
bool     ir_take_event(void);       /* 主循环取事件，取完清除 */

#ifdef __cplusplus
}
#endif

#endif /* IR_H */
