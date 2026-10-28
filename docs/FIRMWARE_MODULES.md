# 固件模块规划（B 部分）

> 原则：**先定接口，再填实现**。每个模块一个 `.c/.h`，先写测试方法，再写代码。
> 分工：B（AI）出设计/接口/测试；**你写核心实现**；B review 并补边界。

---

## 1. 分层

```
app/       业务逻辑（第一阶段演示、第二阶段扫描）
  ↑
drivers/   外设驱动（LED、红外、RGB、电机、索引测量）
  ↑
common/    时钟、SysTick、串口日志、环形缓冲、工具
  ↑
CMSIS/HAL  芯片库（third_party）
```

---

## 2. 模块清单

| # | 模块 | 文件 | 依赖 | 里程碑 | 谁写 |
|---|---|---|---|---|---|
| 1 | 板级初始化 | `common/board.c/h` | HAL | M0 | 我（已给骨架） |
| 2 | 串口日志 | `common/log.c/h`（printf 重定向 + 环形缓冲） | 1 | M0 | 你 |
| 3 | 心跳/延时 | `drivers/led.c/h` | 1 | M0 | 你 |
| 4 | 红外输入 + 消抖 | `drivers/ir.c/h` | 1 | M1 | **你（核心）** |
| 5 | RGB PWM | `drivers/rgb.c/h` | 1 | M2 | **你（核心）** |
| 6 | 电机 PWM | `drivers/motor.c/h` | 1 | M3 | 你 |
| 7 | 串口命令解析 | `app/cmd.c/h` | 2、5、6 | M4 | 你 |
| 8 | 索引周期测量/测速 | `drivers/tacho.c/h` | 4 | M5 | **你（核心）** |
| 9 | 扫描时序 + 帧缓冲 | `app/scan.c/h` | 5、8 | M6 | 我出设计，你实现 |
| 10 | 图案/动画 | `app/pattern.c/h` | 9 | M6 | 你 |
| 11 | 失锁保护 | `app/lock.c/h` | 8、9 | M6 | 我出设计，你实现 |
| 12 | 上位机工具 | `tools/serial_*.py` | 7 | M4+ | 我 |

---

## 3. 关键接口草案（先定这个）

```c
/* ir.h —— M1 核心，你实现 */
void      ir_init(void);                 /* PA1 EXTI 下降沿，上拉 */
uint32_t  ir_count(void);                /* 累计索引脉冲数 */
uint32_t  ir_last_tick_us(void);         /* 最近一次边沿的微秒时间戳 */
bool      ir_take_event(void);           /* 取一次"有效事件"，无则 false */
void      ir_on_edge_isr(void);          /* 中断里调用（只置标志/记时间） */

/* rgb.h —— M2 核心，你实现 */
void rgb_init(void);                     /* TIM3 CH1/2/3，开漏，PWM 反相 */
void rgb_set(uint8_t r, uint8_t g, uint8_t b);   /* 0-255 */
void rgb_set_white(uint8_t level);       /* 白/黑测试用 */

/* motor.h —— M3 */
void     motor_init(void);
void     motor_set_percent(uint8_t pct); /* 0-100 */
void     motor_stop(void);

/* tacho.h —— M5 核心，你实现 */
void     tacho_init(void);               /* 1 MHz 计数 + 输入捕获 */
uint32_t tacho_period_us(void);          /* 最近索引周期（滑动平均） */
uint32_t tacho_rpm(void);

/* scan.h —— M6 */
void scan_init(void);
void scan_frame(const uint8_t frame[16][25][3]);  /* 输出一帧 */
```

---

## 4. 实现顺序（建议）

1. **M1 红外**：EXTI + 消抖 + 1 秒 LED（非阻塞）→ 先用信号源/手挡测试
2. **M2 RGB**：三路 PWM + 8 色 → 手电照灯珠看颜色
3. **M3 电机**：PWM 启停 → 电机空载测试
4. **M4 串口**：命令解析 → PC 串口助手控制
5. **M5 测速**：索引周期 → 示波器/串口看 rpm
6. **M6 扫描**：帧缓冲 + 像素时序 → 整机联调

---

## 5. 每个模块的"完成标准"（写进 issue）

- 编译通过（`text/data` 数字记录）
- 有独立测试方法（串口命令 / 逻辑分析仪 / 现象）
- 边界情况：非法参数、溢出、抖动、失锁
- 代码里注释清楚"为什么"，而不只是"是什么"

---

## 6. 学习分工（你希望多参与）

| 阶段 | 我做什么 | 你做什么 |
|---|---|---|
| 设计 | 写接口 + 状态机图 + 测试用例 | 读懂接口，提出疑问 |
| 实现 | 给骨架（TODO 注释） | **写核心函数实现** |
| 调试 | 帮你看波形/日志、指出问题 | 自己改、自己验证 |
| 收尾 | review + 补边界 + 写文档 | 解释你的设计 |

每完成一个模块，你写 3 句话：「我为什么这样写 / 遇到什么问题 / 怎么验证的」，我帮你对照赛题验收点。

---

## 7. 当前状态

- M0 骨架已在仓库（我写的）
- M1 已完成（`ir.c`：EXTI + 20ms 时间窗消抖 + 事件；main 里 LED 亮 1s 非阻塞）
- M2 已完成（`rgb.c`：8 色表由 target/level 控制，PNP 反相 `compare = 1000 - duty`）
- M3 已完成（`motor.c`：TIM4_CH1，CCR 0–1000 六档；PWM 频率待电机实物确认）
- M4 已完成（2026-10-27）：`uart.c` + `control.c` + `cmd.c`

## 8. M4 串口命令（已实现）

### 分层

| 层 | 文件 | 职责 |
|---|---|---|
| 驱动 | `uart.c/h` | USART2 RX 中断 + 256 字节环形缓冲 + 行缓冲；`printf` 走 TX（`_write` 重定向在 main.c） |
| 状态 | `control.c/h` | 保存 target（R/G/B/M）+ 每路档位（0–5）+ `control_apply()` |
| 命令 | `cmd.c/h` | 解析一行命令，调 control/rgb/motor/ir |

### 命令表（115200 8N1，`\r\n` 结尾）

| 命令 | 作用 | 示例 |
|---|---|---|
| `HELP` | 列出命令 | `HELP` |
| `STATUS` | 打印 target、四路档位、RGB 占空比 | `STATUS` |
| `TARGET R\|G\|B\|M` | 选当前目标 | `TARGET G` |
| `LEVEL 0-5` | 设当前目标档位（0=关，1–5 亮度） | `LEVEL 3` |
| `RGB r g b` | 直接设三路占空比 0–1000 | `RGB 1000 0 0` |
| `MOTOR 0-5` | 电机档位（0=停） | `MOTOR 2` |
| `IR` | 打印红外累计脉冲数 | `IR` |
| `CLR` | 全灭、电机停 | `CLR` |

### 按键与串口共用同一套状态

- KEY1 短按 = `TARGET` 循环
- KEY2 短按 = 当前目标 `LEVEL` +1（0→1→…→5→0）
- 串口改的是同一份 `control` 状态，所以 `STATUS` 能反映按键操作结果

### 验证方法（无板也能看编译；有板用串口）

1. 编译通过（已用 `arm-none-eabi-gcc -Wall -Wextra` 检查 8 个文件，0 warning）
2. 上电 → 串口发 `HELP` 应回命令表
3. `TARGET R` + `LEVEL 3` → 红灯 60% 亮度
4. `RGB 0 1000 0` → 绿灯全亮
5. `MOTOR 3` → 电机 60% 档
6. 按键操作后 `STATUS` 数值应同步变化

### 注意

- USART2 的 NVIC 在 CubeMX 生成代码里**没有使能**（`.ioc` 里有但生成代码没调用），所以 `uart_init()` 里手动 `HAL_NVIC_SetPriority/EnableIRQ(USART2_IRQn)`
- `USART2_IRQHandler` 已在 `stm32f4xx_it.c` 生成（调 `HAL_UART_IRQHandler`），不要重复定义
- 环形缓冲用「留一个空位」判满，256 字节，115200 下约 22 ms 不读才会溢出
