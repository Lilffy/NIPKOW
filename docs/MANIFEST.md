# 资料归档与完整性校验

> 校验日期：2026-10-24
> 目的：确保你给的 3 份指导文档（+1 份交接文档）在归档、抽取、引用过程中**不丢字、不串行、不变形**。

---

## 1. 文件清单与 SHA-256

| 原始文件（Downloads） | 归档路径 | 大小 (B) | SHA-256 |
|---|---|---|---|
| 2026第四届"嘉立创杯"…赛题..pdf | `docs/inbox/contest_problem.pdf` | 596,969 | `9B827DB54FD35291C6C5D7624CCFFFBFDB0E5BAE47051EBE41F8431B9D93B431` |
| 立创梁山派·天空星开发板原理图_2024-01-17..pdf | `docs/inbox/board_schematic.pdf` | 1,367,561 | `8667D4E882F61BDB0DC9279479E69BB98B540CDB87CA1C52074871B34F889BB1` |
| 指导文档.docx | `docs/inbox/guide.docx` | 461,949 | `1DD95D032B5032E97C7C02763E96768DC6AAE62B75AC6B5BBE16E04DAE69F283` |
| 尼普科夫鼓PCB_..md | `docs/inbox/handover.md` | 12,333 | `3D90A6069007D7BB3E55E074C5C537DB8A23D3F8F8FBC3C1DFD625D4EE7D46F1` |

**原文件 ↔ 归档副本逐字节比对：4/4 MATCH**（大小 + SHA-256 全部一致）。

## 2. 抽取结果（纯文本 / 图片）

| 文本 | 字符数 | SHA-256 | 抽取方式 |
|---|---|---|---|
| `docs/text/contest_problem.txt` | 8,727 | `517490DE92C9A728B5F8A42D4D14EF454BAA517633D26FF09A5C487B64F2822E` | pypdf，5 页 |
| `docs/text/guide.txt` | 8,462 | `8161B3C6000EA17ABE7E43B1B4B289AF499E17CF5A8F7C4C0B62282F181B0A6D` | python-docx + 表格，51 段 + 1 表 |
| `docs/text/board_schematic.txt` | 14,337 | `7B2D0A8829B2AA5B2B281D417AF4D496C510EA702B9D16CE92ADE157714808D8` | pypdf，9 页 |

图片：`docs/render/` 下有赛题 5 页、原理图关键页、DOCX 内嵌 4 张图（`guide_image1..4`，其中图 1 是参考电路），均已抽取出原图查看。

## 3. 校验方法（为什么能确认"没出错"）

| 检查 | 方法 | 结果 |
|---|---|---|
| 归档完整性 | 原文件与副本 SHA-256 比对 | ✅ 4/4 一致 |
| PDF 页数 | pypdf 与 PyMuPDF 两套独立解析 | ✅ 赛题 5 页、原理图 9 页，两套一致 |
| PDF 文本 | 两套引擎逐页字符数对比（差异 2–5%，属正常排版空白差异） | ✅ 无缺页、无乱码 |
| 编码 | 全文检索 U+FFFD 替换字符 | ✅ 0 处 |
| DOCX 完整性 | python-docx 段落文本 ↔ `word/document.xml` 原始 `<w:t>` 全文 | ✅ 51 段全部逐字命中，字符数 3261 = 3208(段) + 53(表) |
| 关键事实 | 用 20+ 个锚点字符串（参数/型号/判据）在抽取文本中检索 | ✅ 全部命中（见第 4 节） |

## 4. 关键事实锚点（抽查用）

| 事实 | 出处 |
|---|---|
| 16 孔、孔 1.255 × 1.961 mm、视窗 22.5°/弧长 31.4 mm、鼓 r=80 | 赛题 p1 |
| 1200 rpm → 20 fps、400 像素、t = T/400 = 125 µs | 赛题 p1–p2 |
| 两阶段、8:30 提交、每组 ≤10 分钟 | 赛题 p1 |
| 第一阶段 5 条；第二阶段 7 条；加分 a–e | 赛题 p4 |
| 物料 C5379898 / C2693640 / C498319 / C126027 / C22370035 | 赛题 p5 |
| LM1117-ADJ：R1=240 Ω、R2=720 Ω → 5.0 V | 指导 1.1 |
| RGB：红 150 Ω、绿蓝 100 Ω（15–20 mA）；GPIO 直驱 ≤8 mA | 指导 1.2 |
| 红外发射 200 Ω ≈19 mA；接收 1 kΩ 上拉；遮光=高、透光=低 | 指导 1.3 |
| 1 MHz 计数、T≈50000、±20% 窄脉冲剔除、失锁判据 1.5T | 指导 2.2 / 2.7 |
| P1/P2 各 40 针；**40 = PIN_IN_+5V，38 = +3V3** | 原理图 p7（矢量线段实测） |
| 板载 LDO `SCJA1117B-XXX-A`、基准 `REF3030AIDBZR`、双路 80PIN 排针 | 原理图 p3 / p1 |
| 兼容 STM32F407Vx / GD32F407/470 / AT32F403A/435 的 0 Ω 跳线表 | 原理图 p6 |

## 5. 如何复核（任何时候可重跑）

```powershell
# 1) 原始文件与归档副本是否一致
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\Users\23041\Downloads\指导文档.docx','C:\Users\23041\Downloads\Nipkow\docs\inbox\guide.docx'

# 2) 重新抽取文本（结果应与 docs/text 完全一致）
$py = 'C:\Users\23041\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe'
& $py .tools\pdftext.py docs\inbox\contest_problem.pdf --out docs\text
& $py .tools\docxtext.py

# 3) 深度校验（页数/双引擎/关键串）
& $py .tools\verify_docs.py
& $py .tools\verify_docx.py
```

## 6. 2026-10-24 增补资料

| 文件 | 大小 | SHA-256 | 说明 |
|---|---|---|---|
| `docs/inbox/motor_led_specs.md` | 6,811 | `39483BDB…F3612` | 电机/灯珠"交接补充"——注意：是**待核实清单**，不含数据手册参数 |
| `docs/inbox/pinout_notes.md` | 7,193 | `383050F7…9B607` | 引脚分配建议稿 V1.0（有 2 处编号笔误，见 HANDOVER_REVIEW） |
| `docs/inbox/hardware_list.md` | 6,805 | `82805C7F…204F3` | 硬件清单 V1.0 |
| `docs/inbox/drum_params.md` | 6,065 | `B2B81FD9…34F52` | 鼓参数通用推导（示例值，非项目实测） |
| `docs/inbox/task_points.md` | 11,917 | `21DD328A…4FDCF` | GPT 版任务清单 V1.0（已被 `docs/TASKS.md` V2.0 替代） |
| `Nipkow/sch/Schematic1/P1.esch2` | 1,869,747 | `8D46D07D…CBC9B` | 工作副本原理图（共阴 + J7 串口 + R23 预留 + 分区整理） |
| `Nipkow/pcb/PCB1.epcb2` | 1,605,193 | `59D0DDDB…1C2C4` | 工作副本 PCB（59 器件按 100×90 mm 板框摆放） |

## 7. 说明

- `docs/inbox/` 视为**只读原件区**，任何加工产物写到 `docs/text/`、`docs/render/`、`docs/*.md`。
- 我的"记忆"是分层的：**磁盘原件（哈希锁定）+ 抽取文本 + `PROJECT_BRIEF.md` 摘要 + `INDEX.md` 索引**。
  每次新会话开工前先跑第 5 节第 1 步，任一哈希变化就能立刻发现，不依赖上下文记忆。
