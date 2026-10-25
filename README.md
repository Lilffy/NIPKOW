# NIPKOW — 柱状尼普科夫鼓机械扫描电视

南京理工大学 · 第四届"嘉立创杯"新生电子设计竞赛参赛作品。

用 Ø160×46 mm 的旋转鼓 + 16 个螺旋排布的小孔 + 单颗 RGB 灯，在 1200 rpm 下显示 16×25 彩色图像。

## 当前进度

| 模块 | 状态 |
|---|---|
| 原理图 | ✅ 冻结（共阴 RGB：S8550 PNP 高边；5V 经 JP1 注入核心板） |
| PCB | ✅ 100×90 mm / 2 层 / 59 器件 / 37 网络全部布通 / DRC **0 错误** / 底层 GND 铺铜 |
| 制造文件 | ✅ `hardware/Gerber.zip`、`BOM.csv`、`PickAndPlace.csv` |
| 物料 | ⬜ 待下单（电机/灯珠/传感器在板子生产后到） |
| 固件 | ⬜ 进行中（见 `docs/B_PLAN_AND_GITHUB.md`） |
| 机械 | ⬜ 待装配 |

## 目录

```
docs/       项目文档（任务清单、BOM、原理图说明、协作指南）
hardware/   制造文件与 BOM
firmware/   固件工程（STM32F407）
tools/      上位机 / 测试脚本
```

## 关键文档

- [任务清单 V2.0](docs/TASKS.md)
- [B 部分任务规划 + GitHub 协作指南](docs/B_PLAN_AND_GITHUB.md) ← **队友先读这份**
- [原理图分区图](docs/SCHEMATIC_LAYOUT.md)
- [BOM](docs/BOM.md)
- [项目简报](docs/PROJECT_BRIEF.md)
- [硬件交接说明（A 必读）](docs/A_HANDOVER_NOTES.md)
- [固件模块规划](docs/FIRMWARE_MODULES.md)
- [CubeMX 新建工程指南](docs/CUBEMX_SETUP.md)

## 硬件要点

- 核心板：立创梁山派·天空星 STM32F407VET6（双排 2×20 排针）
- 供电：7.4–12 V（建议 9 V）→ SS34 防反接 → LM1117-ADJ 5 V（注入核心板）/ LM1117-3.3（红外用）
- RGB：共阴，S8550 PNP 高边，GPIO **开漏输出 + PWM 极性取反**
- 索引：红外对管 + 施密特/RC，PA1 EXTI
- 电机：3720 内置驱动无刷电机，PB6 PWM

## 协作方式

- 分支：`feat/a-xxx`（硬件）、`feat/b-xxx`（软件）
- 提交信息：`feat(hw): ...` / `feat(sw): ...` / `docs: ...` / `test: ...`
- 每个任务一个 Issue，完成需附验收证据
- 详细流程见 [B_PLAN_AND_GITHUB.md](docs/B_PLAN_AND_GITHUB.md) 第 4 节
- **两个 AI 协作守则见 [GITHUB_COLLAB_PROTOCOL.md](docs/GITHUB_COLLAB_PROTOCOL.md)**（文件所有权、Issue/PR 规范、每日状态）

## 组内

- A：硬件 / 机械
- B：固件 / 上位机 / 测试
