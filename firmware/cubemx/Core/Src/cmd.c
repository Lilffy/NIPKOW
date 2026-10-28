#include "cmd.h"
#include "uart.h"
#include "control.h"
#include "rgb.h"
#include "motor.h"
#include "ir.h"
#include <stdio.h>
#include <string.h>
#include <ctype.h>

static void to_upper(char *s)
{
    while (*s != '\0') {
        *s = (char)toupper((unsigned char)*s);
        ++s;
    }
}

static void print_help(void)
{
    printf("=== CMD ===\r\n");
    printf("HELP\r\n");
    printf("STATUS\r\n");
    printf("TARGET R|G|B|M\r\n");
    printf("LEVEL 0-5\r\n");
    printf("RGB <r> <g> <b>   (0-1000)\r\n");
    printf("MOTOR 0-5\r\n");
    printf("IR\r\n");
    printf("CLR\r\n");
}

void cmd_poll(void)
{
    char line[96];
    char cmd[12];
    char *p;
    uint8_t n = 0U;

    if (!uart_get_line(line, sizeof(line))) {
        return;
    }

    p = line;
    while (*p == ' ') {
        ++p;
    }
    while ((*p != '\0') && (*p != ' ') && (n < (uint8_t)(sizeof(cmd) - 1U))) {
        cmd[n++] = *p++;
    }
    cmd[n] = '\0';
    while (*p == ' ') {
        ++p;
    }
    to_upper(cmd);

    if (cmd[0] == '\0') {
        return;
    }

    if (strcmp(cmd, "HELP") == 0) {
        print_help();
        return;
    }

    if (strcmp(cmd, "STATUS") == 0) {
        printf("target=%c lvR=%u lvG=%u lvB=%u lvM=%u dutyR=%u dutyG=%u dutyB=%u\r\n",
               "RGBM"[control_target()],
               (unsigned)control_level_of(CONTROL_TARGET_R),
               (unsigned)control_level_of(CONTROL_TARGET_G),
               (unsigned)control_level_of(CONTROL_TARGET_B),
               (unsigned)control_level_of(CONTROL_TARGET_M),
               (unsigned)rgb_get_duty(0),
               (unsigned)rgb_get_duty(1),
               (unsigned)rgb_get_duty(2));
        return;
    }

    if (strcmp(cmd, "TARGET") == 0) {
        char t = (char)toupper((unsigned char)*p);
        int idx = -1;
        if (t == 'R') { idx = CONTROL_TARGET_R; }
        else if (t == 'G') { idx = CONTROL_TARGET_G; }
        else if (t == 'B') { idx = CONTROL_TARGET_B; }
        else if (t == 'M') { idx = CONTROL_TARGET_M; }

        if (idx < 0) {
            printf("ERR target (R|G|B|M)\r\n");
            return;
        }
        control_set_target((uint8_t)idx);
        printf("target=%c\r\n", t);
        return;
    }

    if (strcmp(cmd, "LEVEL") == 0) {
        unsigned lv = 0U;
        if ((sscanf(p, "%u", &lv) != 1) || (lv >= CONTROL_LEVEL_COUNT)) {
            printf("ERR level (0-5)\r\n");
            return;
        }
        (void)control_set_level(control_target(), (uint8_t)lv);
        control_apply();
        printf("level=%u\r\n", lv);
        return;
    }

    if (strcmp(cmd, "RGB") == 0) {
        unsigned r = 0U, g = 0U, b = 0U;
        if (sscanf(p, "%u %u %u", &r, &g, &b) != 3) {
            printf("ERR rgb (0-1000 x3)\r\n");
            return;
        }
        rgb_set_duty(0U, (uint16_t)r);
        rgb_set_duty(1U, (uint16_t)g);
        rgb_set_duty(2U, (uint16_t)b);
        rgb_use();
        printf("rgb=%u,%u,%u\r\n", r, g, b);
        return;
    }

    if (strcmp(cmd, "MOTOR") == 0) {
        unsigned lv = 0U;
        if ((sscanf(p, "%u", &lv) != 1) || (lv >= CONTROL_LEVEL_COUNT)) {
            printf("ERR motor (0-5)\r\n");
            return;
        }
        (void)control_set_level(CONTROL_TARGET_M, (uint8_t)lv);
        motor_set(CONTROL_TARGET_M, (uint8_t)lv);
        printf("motor_level=%u\r\n", lv);
        return;
    }

    if (strcmp(cmd, "IR") == 0) {
        printf("ir_count=%lu\r\n", (unsigned long)ir_count());
        return;
    }

    if (strcmp(cmd, "CLR") == 0) {
        rgb_set_duty(0U, 0U);
        rgb_set_duty(1U, 0U);
        rgb_set_duty(2U, 0U);
        rgb_use();
        (void)control_set_level(CONTROL_TARGET_R, 0U);
        (void)control_set_level(CONTROL_TARGET_G, 0U);
        (void)control_set_level(CONTROL_TARGET_B, 0U);
        (void)control_set_level(CONTROL_TARGET_M, 0U);
        printf("cleared\r\n");
        return;
    }

    printf("ERR unknown: %s\r\n", cmd);
}
