#ifndef UART_H
#define UART_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

void uart_init(void);
bool uart_get_line(char *out, uint16_t maxlen);

#ifdef __cplusplus
}
#endif

#endif /* UART_H */
