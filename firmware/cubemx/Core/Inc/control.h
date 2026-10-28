#ifndef CONTROL_H
#define CONTROL_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define CONTROL_TARGET_R     0U
#define CONTROL_TARGET_G     1U
#define CONTROL_TARGET_B     2U
#define CONTROL_TARGET_M     3U
#define CONTROL_LEVEL_COUNT  6U

void    control_init(void);
uint8_t control_target(void);
void    control_set_target(uint8_t target);
void    control_next_target(void);
void    control_level_step(void);
uint8_t control_level(void);
uint8_t control_level_of(uint8_t target);
bool    control_set_level(uint8_t target, uint8_t level);
void    control_apply(void);

#ifdef __cplusplus
}
#endif

#endif /* CONTROL_H */
