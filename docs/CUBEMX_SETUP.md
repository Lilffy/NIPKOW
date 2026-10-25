# CubeMX 新建工程指南（STM32F407VET6 / 天空星）

> 结论先说：**CubeMX 不需要单独安装 "F407 芯片包"**，器件库是内置的。
> 真正要下载的是 **STM32Cube FW_F4 固件包**（HAL 库），在生成代码时下载。

---

## 0. 现在就开始：10 分钟配好引脚（click 级步骤）

> 没有硬件也能做这一步：CubeMX 配置 + 生成代码 + 编译，就是 M0 的"工程部分"。

**① 建工程**
- `File → New Project` → 搜索框输入 `STM32F407VETx` → 双击选中 → **Start Project**

**② 开外部晶振**
- 左侧 `System Core → RCC` → **HSE** 选 `Crystal/Ceramic Resonator`

**③ 配时钟（Clock Configuration 页）**
- 依次点击/修改：`HSE=8`、`PLL Source=HSE`、`PLLM=8`、`PLLN=336`、`PLLP=2`
- `System Clock Mux` 选 `PLLCLK`
- `AHB Prescaler=/1`、`APB1=/4`、`APB2=/2`
- 看到 **HCLK=168、PCLK1=42、PCLK2=84** 就对了

**④ 配引脚（Pinout 视图，直接点芯片图上的引脚）**

| 引脚 | 点它 → 选 | 参数 |
|---|---|---|
| PA2 | `USART2_TX` | 左侧 `Connectivity → USART2 → Mode=Asynchronous`，Baud=115200, 8N1 |
| PA3 | `USART2_RX` | 同上 |
| PA6 | `TIM3_CH1` | `Timers → TIM3 → Clock Source=Internal Clock`；Channel1~3 都选 `PWM Generation CHx` |
| PA7 | `TIM3_CH2` | 同上 |
| PB0 | `TIM3_CH3` | 同上 |
| PB6 | `TIM4_CH1` | `Timers → TIM4 → Channel1 = PWM Generation CH1` |
| PA1 | `GPIO_EXTI1` | `System Core → GPIO → PA1`：Mode=`External Interrupt Mode with Falling edge trigger detection`，Pull=`Pull-up` |
| PB2 | `GPIO_Output` | PA2 名下的设置：Mode=`Output Push Pull`，初始电平 `Low`，Speed=`Low` |
| PC0 | `GPIO_Input` | Pull=`Pull-up` |
| PC1 | `GPIO_Input` | Pull=`Pull-up` |

**⑤ 参数细节**
- `TIM3`：`Prescaler=167`、`Counter Period(ARR)=999` → PWM 1 kHz（168MHz/(167+1)/(999+1)）
- `TIM4`：同样 `167 / 999` → 1 kHz（后面按电机实物再调）
- `SYS → Debug` 选 **Serial Wire**（否则下载一次就锁死 SWD）
- `NVIC` 里勾上 **EXTI line1 interrupt**（M1 要用）

**⑥ 必须关掉的东西**
- `Connectivity → SPI1` 保持 **Disabled**（PA6/PA7 被 TIM3 占用；板载 SPI Flash 是共用的）
- 不要开 `USB`、`ETH`、`SDIO` 等不用的外设

**⑦ 生成**
- `Project Manager`：Project Name=`nipkow-m0`，Toolchain/IDE=**CMake**
- `Code Generator` 勾 `Generate peripheral initialization as a pair of '.c/.h' files per peripheral`
- 点 **GENERATE CODE**

**⑧ 检查生成结果**
打开生成的 `Core/Src/main.c`，确认有：
- `MX_GPIO_Init()`、`MX_USART2_UART_Init()`、`MX_TIM3_Init()`、`MX_TIM4_Init()`
- `SystemClock_Config()` 里 `PLLM=8, PLLN=336, PLLP=RCC_PLLP_DIV2`
- 编译一次（VSCode CMake 或命令行），能出 `.elf` 即成功

> 做完这 8 步，你的 M0"工程骨架"就有了。之后和我写的 `firmware/` 对照，看差异在哪、为什么。

---

## 1. 新建工程

1. 打开 `D:\STM32\STM32CubeMX.exe`
2. **File → New Project**
3. 在搜索框输入 **`STM32F407VETx`**（VET6 = LQFP100，512K Flash）
   - 在列表里选 **STM32F407VETx**，双击 → 进入配置界面
   - ⚠️ 如果搜不到，检查 `Help → Manage embedded software packages` 里 MCU 数据库是否完整；CubeMX 6.15 自带 F4 全系列
4. 第一次生成代码时会提示下载 **STM32Cube MCU Package for STM32F4**：
   - `Help → Manage embedded software packages` → 选 `STM32Cube MCU Package for STM32F4` → **Install**
   - 需要 ST 账号登录 + 网络（建议开代理）
   - 下载失败就点 **From Local**，用官方 `stm32cube_fw_f4_vX.Y.Z.zip`

---

## 2. 时钟配置（必须和代码一致）

**RCC（Pinout 页）**
- HSE：**Crystal/Ceramic Resonator**（天空星板载 8 MHz 晶振）
- LSE：Disable（原理图有 32.768k，但第一阶段用不到）

**Clock Configuration 页**
| 项 | 值 |
|---|---|
| HSE 输入 | 8 MHz |
| PLL Source | HSE |
| PLLM | 8 |
| PLLN | 336 |
| PLLP | 2 |
| PLLQ | 7 |
| SYSCLK | **168 MHz** |
| AHB 分频 | /1（168 MHz） |
| APB1 分频 | /4（42 MHz） |
| APB2 分频 | /2（84 MHz） |
| Flash Latency | 5 WS |
| Voltage Scale | Scale 1 |

---

## 3. 引脚配置

| 引脚 | 功能 | CubeMX 设置 |
|---|---|---|
| PA2 | USART2_TX | Connectivity → USART2 → Asynchronous（115200 8N1） |
| PA3 | USART2_RX | 同上 |
| PA6 | TIM3_CH1（R_PWM） | Timers → TIM3 → Channel1 = PWM Generation CH1 |
| PA7 | TIM3_CH2（G_PWM） | Channel2 = PWM Generation CH2 |
| PB0 | TIM3_CH3（B_PWM） | Channel3 = PWM Generation CH3 |
| PB6 | TIM4_CH1（电机 PWM） | Timers → TIM4 → Channel1 = PWM Generation CH1 |
| PA1 | IR_INDEX | GPIO_EXTI1，**下降沿触发**，上拉 |
| PB2 | 用户 LED | GPIO_Output，**初始低电平**（高电平点亮） |
| PC0/PC1 | KEY1/KEY2 | GPIO_Input，Pull-up |
| PA13/PA14 | SWD | 默认保留（不要禁用） |

**PWM 频率建议**：
- TIM3（RGB）：预分频后 1–5 kHz 即可（灯珠人眼无频闪要求不高）；内部再调占空比
- TIM4（电机）：按实物电机/驱动要求，先设 50 Hz–1 kHz，实测再调

> ⚠️ RGB 是 **PNP 高边驱动**：GPIO 必须配置为 **Open-Drain**（CubeMX 里 GPIO 设置 Output → Open Drain），并且 PWM 占空比要**取反**（占空比越大越暗）。这一点 CubeMX 不会自动帮你，必须在代码里处理。

---

## 4. 生成代码

**Project Manager 页**
1. Project Name：`nipkow-m0`
2. Toolchain/IDE：
   - **CMake**（推荐，配你的 VSCode + CMake Tools）
   - 或 STM32CubeIDE（用 ST 的 VS Code 扩展）
3. Code Generator：
   - ☑ Generate peripheral initialization as a pair of '.c/.h' files
   - ☑ Keep User Code when re-generating

点 **GENERATE CODE**。

---

## 5. 两条路，二选一

### 路线 A（推荐先用）：直接用仓库工程
仓库 `firmware/` 已经有完整 CMake 工程 + HAL + M0 代码，**不需要 CubeMX**：

```powershell
cd firmware
cmake -B build -G Ninja
cmake --build build
```

需要 `arm-none-eabi-gcc`、CMake、Ninja 在 PATH（工具已放在 `.tools/bin/`）。

### 路线 B：CubeMX 生成后再合并
1. CubeMX 按上面配置生成 `nipkow-m0`
2. 把生成工程和仓库 `firmware/` 对比：
   - 引脚初始化（`gpio.c` / `tim.c` / `usart.c`）用 CubeMX 生成的
   - `main.c` 里的心跳/printf 逻辑照抄我们的 `Core/Src/main.c`
3. 好处：外设参数可视化、以后加外设方便

> 不管走哪条，**引脚定义以本文件和 `docs/SCHEMATIC_LAYOUT.md` 为准**，不要自己改。

---

## 6. 常见问题

| 现象 | 原因 | 解决 |
|---|---|---|
| 搜不到 STM32F407VETx | 数据库未加载 | Help → Manage embedded software packages → 检查 MCU Database |
| 生成时卡在下载 FW 包 | 网络/未登录 ST | 开代理 + 登录；或 From Local 装 zip |
| `arm-none-eabi-gcc` 找不到 | 没在 PATH | 加 `C:\Users\23041\Downloads\arm-gnu-toolchain-...\bin` |
| CMake 配置卡住 | 少见（杀软/路径含空格） | 换到纯英文无空格路径；或先用路线 A 的脚本 |
| 编译报 `undefined reference to _write` | 没加 printf 重定向 | 照抄 `firmware/Core/Src/main.c` 的 `_write` |
