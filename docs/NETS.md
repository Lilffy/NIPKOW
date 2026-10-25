# 原理图网表（从 .esch2 文件重建）

> 生成时间：2026-10-24 23:47（共阴 + J7 串口 + R23 预留 + 分区整理）
> 工具：`.tools/netlist.py`（读 V3 日志格式 → 线段聚类 + 网络标签合并 → 引脚映射）
> 说明：这是"设计意图网表"，用于审查；最终以 EDA 的 ERC/网表导出为准。
segments=147 clusters=37 components=60 pins=212

[GND] 33 pins
    ?.1  Pin1
    C1.2  2
    C10.2  2
    C2.2  2
    C3.2  2
    C4.2  2
    C5.2  2
    C6.2  2
    C7.2  2
    C8.2  2
    C9.2  2
    J1.2  2
    J3.4  4
    J4.2  2
    J5.2  2
    J6.2  2
    J7.1  1
    KEY1.3  3
    KEY2.3  3
    Q1.2  S
    Q2.2  S
    Q3.2  S
    R11.2  2
    R16.2  2
    R2.2  2
    R5.2  2
    R8.2  2
    TP4.1  1
    U1.37  AGND
    U1.39  GND
    U1.77  GND
    U1.79  GND
    U2.1  GND

[+5V_REG] 13 pins
    C4.1  1
    C8.1  1
    JP1.1  1
    Q4.2  E
    Q5.2  E
    Q6.2  E
    R10.2  2
    R12.1  1
    R20.1  1
    R21.1  1
    R22.1  1
    TP2.1  1
    U3.2  VOUT

[VIN_PROTECTED] 11 pins
    C1.1  1
    C10.1  1
    C3.1  1
    C5.1  1
    C7.1  1
    C9.1  1
    D1.2  K
    J6.1  1
    TP1.1  1
    U2.3  VIN
    U3.3  VIN

[+3V3_EXT] 9 pins
    C2.1  1
    C6.1  1
    R13.1  1
    R14.1  1
    R16.1  1
    R23.1  1
    TP3.1  1
    U2.2  VOUT
    U2.4  VOUT

[IR_INDEX] 5 pins
    D2.1  K
    J5.1  1
    R13.2  2
    TP5.1  1
    U1.4  PA1

[MOTOR_PWM] 3 pins
    J6.3  3
    TP9.1  1
    U1.63  PB6

[+3V3_CORE] 3 pins
    R15.2  2
    U1.38  +3V3
    U1.78  +3V3

[R_PWM] 3 pins
    R17.1  1
    TP6.1  1
    U1.7  PA6

[G_PWM] 3 pins
    R18.1  1
    TP7.1  1
    U1.10  PA7

[B_PWM] 3 pins
    R19.1  1
    TP8.1  1
    U1.11  PB0

[R_BASE] 3 pins
    Q4.1  B
    R17.2  2
    R20.2  2

[R_DRV] 3 pins
    Q1.3  D
    Q4.3  C
    R3.2  2

[G_BASE] 3 pins
    Q5.1  B
    R18.2  2
    R21.2  2

[G_DRV] 3 pins
    Q2.3  D
    Q5.3  C
    R6.2  2

[B_BASE] 3 pins
    Q6.1  B
    R19.2  2
    R22.2  2

[B_DRV] 3 pins
    Q3.3  D
    Q6.3  C
    R9.2  2

[ADJ] 3 pins
    R10.1  1
    R11.1  1
    U3.1  ADJ

[+5V_CORE] 3 pins
    JP1.2  2
    U1.40  +5V0
    U1.80  +5V0

[PA4] 2 pins
    R15.1  1
    U1.5  PA4

[UART_TX] 2 pins
    J7.2  2
    U1.1  PA2

[UART_RX] 2 pins
    J7.3  3
    U1.6  PA3

[UART_VCC] 2 pins
    J7.4  4
    R23.2  2

[(unnamed)] 2 pins
    Q1.1  G
    R2.1  1

[RGB_R_K] 2 pins
    J3.1  1
    R3.1  1

[RGB_G_K] 2 pins
    J3.2  2
    R6.1  1

[(unnamed)] 2 pins
    Q2.1  G
    R5.1  1

[RGB_B_K] 2 pins
    J3.3  3
    R9.1  1

[(unnamed)] 2 pins
    Q3.1  G
    R8.1  1

[VIN_MAIN] 2 pins
    D1.1  A
    J1.1  1

[IR_TX_A] 2 pins
    J4.1  1
    R12.2  2

[(unnamed)] 2 pins
    D2.2  A
    R14.2  2

[KEY1] 2 pins
    KEY1.2  2
    U1.54  PC0

[KEY2] 2 pins
    KEY2.2  2
    U1.55  PC1

[MOTOR_AUX] 1 pins
    J6.5  5

[EXP_IO1] 1 pins
    U1.56  PC2

[EXP_IO2] 1 pins
    U1.57  PC3

[MOTOR_FG] 1 pins
    J6.4  4

unused pins: 68

