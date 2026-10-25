# 文档索引

最后一版：2026-10-24

| 路径 | 内容 | 关键位置 |
|---|---|---|
| `docs/inbox/contest_problem.pdf` | 赛题原文（5 页） | p1 任务与几何；p2 方案/框图/核心板；p3 扩展板要求/机械参数；p4 两阶段验收 7 条+加分；p5 元器件表 |
| `docs/inbox/guide.docx` | 指导文档（组委/学长版实施指导，51 段+1 表） | 1.1 电源；1.2 RGB；1.3 光电；1.4 按键/测试点；1.5 电机；1.6 PCB/焊接；1.7 软件台阶；2.1–2.7 第二阶段逐项做法 |
| `docs/inbox/board_schematic.pdf` | 「立创梁山派·天空星」开发板原理图（9 页，V1.0 2024-01-17） | p1 层次总图；p2 按钮/LED；p3 供电/USB；p4 TF+FLASH；p5 LQFP-100 引脚分配；p6 供电脚/兼容跳线；p7 双 40PIN 排针；p8 10 针调试口；p9 螺丝孔 |
| `docs/text/*.txt` | 三份文档的可检索纯文本（PDF 用 pypdf 抽取，DOCX 用 python-docx） | 与原文页码对应 |
| `docs/render/*.png` | 关键页/关键图渲染图 | `contest_problem_p1..p5`、`board_schematic_p1`、`guide_image1..4`（含 `guide_rx_zoom` 放大图） |
| `docs/PROJECT_BRIEF.md` | **项目摘要（先读这个）**：参数表、电路要求、固件台阶、风险、待确认 | |
| `docs/HANDOVER_REVIEW.md` | **交接文档对照审查**：与我的方案冲突、5V/3V3 脚号纠正、新发现隐患、接手方式 | 2026-10-24 |
| `docs/MANIFEST.md` | **资料归档完整性校验**：SHA-256、抽取统计、双引擎校验、关键事实锚点、复核命令 | 2026-10-24 |
| `docs/CHANGELOG.md` | **对工作副本的每次编辑**：改了什么、备份路径、前后哈希、回滚命令 | 2026-10-24 |
| `docs/NETS.md` | **从 .esch2 重建的网表**（设计意图网表，用于审查） | 2026-10-24 |
| `docs/DESIGN_PLAN.md` | **阶段一收尾计划**：哪些现在冻结/哪些等实物、预估阻值、TBD 清单、收尾顺序 | 2026-10-24 |
| `docs/BOM.md` + `docs/BOM_draft.csv` | **物料清单**（分组 + 采购待办）与明细 CSV | 2026-10-24 |
| `docs/SCHEMATIC_LAYOUT.md` | **原理图分区图**：各区位置、J7 串口定义、备注 | 2026-10-24 |
| `docs/TASKS.md` | **任务清单 V2.0**（替代 GPT 版任务点）：变更摘要、现状、P0/P1/P2 待办、里程碑、风险、分工 | 2026-10-25 |
| `docs/B_PLAN_AND_GITHUB.md` | **给队友 DeepSeek 的协作包**：项目一页纸、分工、B 部分任务规划、GitHub 首次配置/日常流程/排错/兜底 | 2026-10-25 |
| `Nipkow/` | 你复制来的 EDA 工程工作副本（我直接改这里） | 2026-10-24 |
| `docs/BOARD_PINOUT.md` | 核心板 80 针排针 → MCU 引脚 → 网络 映射表 | 待补（见 HANDOVER_REVIEW §2.1） |
| `docs/QUESTIONS.md` | 待确认清单（阻塞项） | |
| `.tools/` | 本地工具链：`pdftext.py`（PDF→txt）、`docxtext.py`、`render.py`（PDF→PNG）、`pylibs/`（pypdf、PyMuPDF，未装系统） | 不进入交付物 |

## 快速用法

```powershell
$py = 'C:\Users\23041\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe'
& $py .tools\pdftext.py docs\inbox\xxx.pdf --out docs\text      # PDF 抽文本
& $py .tools\render.py  docs\inbox\xxx.pdf docs\render --pages 3 --dpi 150   # 渲染页面
```

## 原始文件名对照

- 立创梁山派·天空星开发板原理图_2024-01-17..pdf → `docs/inbox/board_schematic.pdf`
- 2026第四届“嘉立创杯”南京理工大学新生电子设计竞赛赛题..pdf → `docs/inbox/contest_problem.pdf`
- 指导文档.docx → `docs/inbox/guide.docx`
