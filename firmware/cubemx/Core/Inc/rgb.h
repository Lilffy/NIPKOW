#ifndef RGB_H
#define RGB_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void rgb_init(void);
void rgb_set(uint8_t target,uint16_t level);
void rgb_use(void);
void rgb_set_duty(uint8_t ch, uint16_t duty);
uint16_t rgb_get_duty(uint8_t ch);
#ifdef __cplusplus
}
#endif

#endif /* RGB_H */