# M0 动手手册（我们一起做）

> 目标：把"最小可运行系统"从零跑通，理解每一步在干什么。
> 我写的 `firmware/` 代码**保留**作为参考，你按下面步骤自己走一遍，遇到卡点我们再一起看。

---

## M0 要达成什么

| # | 验收项 | 现象 |
|---|---|---|
| 1 | 程序能下载 | ST-Link 下载成功，无报错 |
| 2 | 时钟 168 MHz | 串口打印 `SYSCLK = 168000000` |
| 3 | 串口 115200 | PC 串口助手能看到文字 |
| 4 | 心跳灯 | PB2 LED 1 Hz 闪烁 |
| 5 | 版本信息 | 上电打印 `=== NIPKOW M0-v0.1 ===` |

---

## 准备清单

**硬件**
- 天空星 STM32F407VET6 核心板
- ST-Link V2（或 DAP-Link）
- USB-TTL（CH340/CP2102 都行）——核心板调试口用
- 杜邦线、USB 线

**接线（核心板 SWD）**
| ST-Link | 核心板 |
|---|---|
| SWDIO | PA13 |
| SWCLK | PA14 |
| GND | GND |
| 3V3 | 3V3（可选，核心板也可 USB 供电） |

**串口（先用核心板自带的 USB 调试口）**
- 天空星的调试口一般板载了 USB 转串口（PA9/PA10 = USART1）
- 如果我们要用 USART2（PA2/PA3），需要 USB-TTL：TX→PA3、RX→PA2、GND→GND

**软件**
- arm-none-eabi-gcc（已装在 `C:\Users\23041\Downloads\arm-gnu-toolchain-...`）
- CMake + Ninja（已放在 `.tools/bin/`）
- VSCode + CMake Tools + C/C++ 插件
- 串口助手（VSCode 的 Serial Monitor 插件即可）

---

## 从哪入手：按这个顺序走

### 第 0 步：看懂工程结构（15 分钟）
打开 `firmware/`，只读不改：

```
Core/
  Src/main.c        ← 主逻辑：时钟、串口、循环
  Src/stm32f4xx_it.c ← 中断：SysTick、EXTI
  Startup/startup_stm32f407xx.s  ← 启动文件（不用改）
  Inc/stm32f4xx_hal_conf.h       ← HAL 配置（HSE_VALUE=8000000）
third_party/
  STM32F4xx_HAL_Driver/  ← ST 的 HAL 库
  CMSIS/                 ← 内核头文件
CMakeLists.txt
```

**要能回答**：
1. 程序从哪开始执行？（`Reset_Handler` → `main`）
2. `HAL_Init()` 做了什么？
3. `SystemClock_Config()` 里 PLL 参数怎么算的？

### 第 1 步：点亮 LED（PB2，高电平亮）
**读**：`Core/Inc/main.h` 的 LED 宏、`main.c` 的 `MX_GPIO_Init()`

**你做**：
1. 新建 `firmware/Core/Src/led_test.c`（或直接在 main.c 里改）
2. 只做三件事：开 GPIOB 时钟、PB2 配推挽输出、循环里 `HAL_GPIO_WritePin(GPIOB, GPIO_PIN_2, GPIO_PIN_SET)` 然后 delay
3. 下载，看 LED 亮不亮

**验证**：灯亮 = 成功；不亮先查：
- 是不是配成了低电平点亮（原理图是 **高电平点亮**）
- PB2 有没有被别的功能占用（BOOT1）

### 第 2 步：串口打印（USART2，115200）
**读**：`main.c` 的 `MX_USART2_UART_Init()` 和 `_write()`

**你做**：
1. 配 PA2/PA3 为 AF7
2. `HAL_UART_Init()` 115200 8N1
3. 实现 `int _write(int, char*, int)` 调用 `HAL_UART_Transmit`
4. `printf("hello\r\n")`

**验证**：串口助手 115200 看到 hello；乱码 → 波特率/时钟错

### 第 3 步：时钟配置（168 MHz）
**读**：`main.c` 的 `SystemClock_Config()`

**你做**：
1. 先跑默认 16 MHz（HSI），打印 `HAL_RCC_GetHCLKFreq()`，确认是 16000000
2. 再改 HSE 8 MHz + PLL（M8/N336/P2），重新打印，确认 168000000
3. 如果卡死：先检查 HSE 是否起振（`HAL_RCC_OscConfig` 返回值）

**验证**：串口打印 168000000；LED 闪烁频率是否变快（同延时下）

### 第 4 步：合成为 M0
把上面三步合起来：
- 168 MHz
- 串口打印版本 + 时钟
- PB2 心跳 1 Hz（用 `HAL_GetTick()` 非阻塞）

**验证**：上电后串口看到：
```
=== NIPKOW M0-v0.1 ===
SYSCLK = 168000000 Hz
...
[hb] tick=1000 led=1
```
灯同步闪。

---

## 调试技巧（卡住先看这里）

| 现象 | 先查 |
|---|---|
| 下载报错 | ST-Link 接线、目标板供电、SWD 是否被禁用 |
| 程序不跑 | 是否进了 HardFault（断点 / 看 PC） |
| 串口无输出 | TX/RX 是否交叉、波特率、时钟是否对 |
| 串口乱码 | 时钟频率和串口配置不匹配 |
| LED 不亮 | 高低电平搞反、引脚错、没开时钟 |
| 卡在 `HAL_RCC_OscConfig` | 晶振没起振（HSE 8 MHz，检查焊接） |

**用 ST-Link 调试**：VSCode + Cortex-Debug 插件，打断点看 `SystemCoreClock`、`uwTick`。

---

## 提交方式

```powershell
git checkout -b feat/b-m0-你的名字
git add -A
git commit -m "feat(sw): M0 自测——LED/串口/时钟"
git push -u origin feat/b-m0-你的名字
```

然后在 GitHub 开 PR，描述里写：**每步验证结果 + 遇到的问题 + 怎么解决的**。

---

## 我们的配合方式

1. 你先走第 1、2 步（最容易看到效果）
2. 卡住就把现象/截图发我，我帮你定位
3. 第 3 步时钟配置最容易出问题，我可以给你讲 PLL 计算过程
4. 全部通过后，我们一起 review 你的代码，再进 M1（红外）

> 记住：**我的代码只是参考答案**，你写的时候可以不一样，只要验收通过、能解释为什么这么写。
