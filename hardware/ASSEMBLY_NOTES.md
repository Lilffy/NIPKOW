# 装配参考图（V1，2026-10-27 从 EDA 导出）

> 用途：A 焊接/装配对位。图上位号与实物丝印一致（同一次 Gerber 导出）。
> 完整 PDF（含顶/底装配图 + 丝印位号图 + BOM + 钻孔图）：`hardware/silk_assembly.pdf`

## 图

| 文件 | 内容 |
|---|---|
| `hardware/assembly_top.png` | **装配图顶层**（器件位置 + 位号 + 极性标记，推荐打印） |
| `hardware/assembly_bottom.png` | 装配图底层 |
| `hardware/silk_top.png` | 顶面自动位号图 |
| `hardware/silk_bottom.png` | 底面自动位号图 |
| `hardware/schematic.pdf` | 原理图 |

## 关键接口接线（焊接前核对）

| 接口 | 定义 |
|---|---|
| **J1** 电源 | 1 = +VIN（7–12V，**建议 9V**），2 = GND |
| **J3** RGB（共阴） | 1 = 红阳极、2 = 绿阳极、3 = 蓝阳极、**4 = GND（公共阴极）** |
| **J4** 红外发射 | 1 = 阳极（长脚，经 R12 到 +5V）、2 = GND（阴极） |
| **J5** 红外接收 | 1 = 集电极 C（接 R13/PA1/TP5）、2 = 发射极 E（GND） |
| **J6** 电机 | 1 = VIN、2 = GND、3 = PWM（PB6）、4 = FG、5 = AUX（预留） |
| **J7** 串口 | 1 = GND、2 = PA2(TX)、3 = PA3(RX)、4 = UART_VCC（R23 默认不贴） |
| **JP1** | 短接 = 扩展板 5V 注入核心板；不短接 = 核心板独立供电 |

### J7 串口接线（调试必用）

买 **CH340/CP2102 USB-TTL 模块（3.3V 电平）** + 杜邦线 3 根：

```
USB-TTL TX  → J7-3 (PA3, 板 RX)
USB-TTL RX  ← J7-2 (PA2, 板 TX)
USB-TTL GND → J7-1 (GND)        ← 必须共地
USB-TTL VCC   不接（R23 不贴，J7-4 无 3.3V 输出）
```

串口参数：**115200 8N1**。上电应看到：

```
=== NIPKOW M0 ===
SYSCLK = 168000000 Hz
HCLK   = 168000000 Hz
```

没输出/乱码排查顺序：GND 共地 → TX/RX 是否交叉 → 模块 3.3V 档 → 波特率。

## 关键测试点

| TP | 网络 | 说明 |
|---|---|---|
| TP1 | VIN_PROTECTED | 防反接后输入 |
| TP2 | +5V_REG | 稳压输出 5V |
| TP3 | +3V3_EXT | 3.3V |
| TP4 | GND | — |
| TP5 | **IR_INDEX** | 红外接收输出（遮光≈3.3V / 通光<0.99V） |
| TP6 | R_PWM | PA6 |
| TP7 | G_PWM | PA7 |
| TP8 | B_PWM | PB0 |
| TP9 | MOTOR_PWM | PB6 |

## 焊接提示

- U3（TO-220）建议装 **10×10×8 散热片 + 绝缘垫片**（背板是 5V 电位，不能碰 GND/外壳）
- R12 建议焊 **220Ω**（原 200Ω 时 If≈18.5mA，接近额定 20mA）
- 弱光时 R13 可换 **2.2k**（原 1k）
- Q1–Q3（AO3400A）+ R2/R5/R8 **DNP 不贴**；R23 **DNP 不贴**
- 详细见 `docs/A_HANDOVER_NOTES.md` 与 `docs/IR_DEVICE_CHECK.md`
