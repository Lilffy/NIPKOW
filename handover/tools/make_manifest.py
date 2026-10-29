# -*- coding: utf-8 -*-
"""
扫描工作区并生成 docs/MANIFEST.md（文件清单 + SHA-256）。

用法： python make_manifest.py
说明： 头部说明与"已丢失产物"清单是静态文本，文件表是自动生成的。
"""

import hashlib
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
DOCS = os.path.join(WS, "docs")

SKIP_DIRS = {"__pycache__", ".git", "dist"}
SKIP_PREFIX = (".dsh-office",)


def sha256(path, n=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(n)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def walk(root):
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(SKIP_PREFIX)]
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root).replace("\\", "/")
            if rel in ("docs/MANIFEST.md",):
                continue
            try:
                st = os.stat(p)
            except OSError:
                continue
            rows.append((rel, st.st_size, sha256(p)[:16], st.st_mtime))
    rows.sort()
    return rows


def human(n):
    if n < 1024:
        return "%d B" % n
    if n < 1024 * 1024:
        return "%.1f KB" % (n / 1024.0)
    return "%.1f MB" % (n / 1024.0 / 1024.0)


HEADER = """# MANIFEST — 文件清单与来源

> 自动生成：`.tools/make_manifest.py`（重新生成会刷新哈希，别手改文件表）
> 快照时间：{when}
> 哈希算法：SHA-256（表里只显示前 16 位，用于快速比对）

## 1. 工程本体（EDA，不在本工作区）

| 文件 | 路径 | 说明 |
|---|---|---|
| EDA 工程 | `C:\\Users\\24707\\Documents\\LCEDA-Pro\\projects\\扩展板1.eprj2` | 嘉立创 EDA 专业版，原理图 + PCB。**内容加密存储，程序无法直接读写**，只能用 GUI 改 |
| 工程快照 | `backup/扩展板1.eprj2.orig`、`Nipkow/扩展板1.eprj2` | 2026-10-25 19:19 复制，SHA-256 见下表 |

## 2. 工作区文件

| 文件 | 大小 | SHA-256(16) | 说明 |
|---|---|---:|---|
"""

FOOTER = """
## 3. 重新生成

```powershell
$py = 'C:\\Users\\24707\\.dsh\\dsh-runtimes\\dsh-primary-runtime\\dependencies\\python\\python.exe'
& $py 'C:\\旋转电视\\.tools\\make_board_dxf.py'   # 板框/孔 DXF + 预览
& $py 'C:\\旋转电视\\.tools\\make_bom.py'        # BOM.md + BOM_draft.csv
& $py 'C:\\旋转电视\\.tools\\make_manifest.py'   # 本文件
```

## 4. 已丢失、需要重建的历史产物

TASKS.md 提到的以下文件在本机已不存在（工作区为空、回收站无、全盘搜索无）：

- `docs/NETS.md`（网表比对结果）、`.tools/netlist.py`（网表工具）
- `docs/BOM.md` + `BOM_draft.csv` 的原始 59 项明细（本工作区已按位号重建为 58 项草稿，差 1 项待核）
- `docs/HANDOVER_REVIEW.md`、`docs/SCHEMATIC_LAYOUT.md`、`docs/CHANGELOG.md`（已新建）

重建方式：先从 EDA 导出 BOM/网表，再对照本工作区的表结构补齐。**不要凭记忆重写位号/参数**。
"""

NOTES = {
    "backup/扩展板1.eprj2.orig": "EDA 工程原始快照（改动前）",
    "Nipkow/扩展板1.eprj2": "EDA 工程第二份拷贝",
    "README.md": "工作区说明与下一步",
    "docs/PCB_P0_PLAYBOOK.md": "★ 板框/安装孔/装配核对/出图下单",
    "docs/ROUTING.md": "★ 线宽、关键路径、地策略、电气复核",
    "docs/RISKS.md": "★ 风险登记册",
    "docs/TEAM_SPLIT.md": "★ 两人分工方案（时间线/接口表/验收对照）",
    "docs/A_STAGE1_TASKS.md": "★ A 的第一阶段清单（焊接/测量/交接包/issue）",
    "docs/A_新手行动手册.md": "★ A 的新手版行动手册（通俗、照着做）",
    "docs/A_新手一周学习计划.md": "★ 等板这一周的 7 天学习计划",
    "docs/A_打印包.pdf": "★★ 12 页打印包（焊接/上电/记录/采购/分块图）",
    "docs/purchase/采购清单.md": "★ 需自购清单（剔除主办方提供件）",
    "docs/purchase/立创BOM导入.csv": "★ 可直接导入立创商城 BOM 配单",
    "docs/purchase/采购清单.csv": "采购清单 CSV",
    "docs/A_打印包.docx": "打印包源文件（可改）",
    "docs/LETTER_TO_B.md": "★ 给 B 的信（贴仓库用：3 个问题 + 10 项清单）",
    "docs/B仓库阅读报告.md": "★ B 仓库阅读结论（BOM/C10/C1C3/文档矛盾）",
    "docs/打板下单.md": "★ 打板下单包（Gerber 核验 + 参数 + 检查清单）",
    "docs/原理图怎么看.md": "★ 原理图为什么看着糙 + 4 张分块图索引 + 读图原则",
    "docs/hardware/NIPKOW_Gerber.zip": "制造文件（上传嘉立创）",
    "docs/hardware/gerber_preview.png": "Gerber 渲染预览",
    "docs/hardware/schematic_扩展板原理图.pdf": "B 导出的扩展板原理图（A0 画布）",
    "docs/hardware/BOM_latest.csv": "最新 BOM（C10 改 10µF/25V）",
    "docs/hardware/PickAndPlace_latest.csv": "最新坐标文件",
    "docs/hardware/PCBInfo_latest.txt": "最新 PCB 信息",
    ".tools/gerber_view.py": "Gerber/钻孔解析 + 预览渲染",
    "docs/refs/B_计划与GitHub指南.md": "B 写的固件里程碑与 GitHub 协作规范",
    "docs/refs/赛题_2026第四届.pdf": "赛题原文（验收标准）",
    "docs/refs/天空星核心板原理图.pdf": "核心板原理图（排针/电源依据）",
    "docs/BOM.md": "器件清单 + 立创编号（已核验）",
    "docs/BOM_draft.csv": "BOM 草稿（可导入表格/商城）",
    "docs/CHANGELOG.md": "改动日志",
    "docs/mech/board_100x90.dxf": "板框 100×90 + 4×M3（导入 EDA 用）",
    "docs/mech/board_99x89.dxf": "备用：单边严格 <100 mm",
    "docs/mech/preview_100x90.png": "板框预览图",
    "docs/mech/preview_99x89.png": "备用方案预览图",
    ".tools/make_board_dxf.py": "生成板框 DXF",
    ".tools/make_bom.py": "生成 BOM",
    ".tools/make_manifest.py": "生成本文件",
    "docs/refs/TASKS_v2.0.md": "任务清单 V2.0 副本",
    "docs/refs/任务点V1.0-已归档.md": "V1.0 任务点（已归档）",
    "docs/refs/引脚分配.md": "引脚分配建议稿（排针号来源）",
    "docs/refs/硬件清单.md": "硬件清单 V1.0",
    "docs/refs/鼓参数.md": "鼓/光学参数",
}


def main():
    rows = walk(WS)
    when = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    out = [HEADER.format(when=when)]
    for rel, size, h, _ in rows:
        note = NOTES.get(rel, "")
        out.append("| `%s` | %s | `%s` | %s |\n" % (rel, human(size), h, note))
    out.append(FOOTER)

    path = os.path.join(DOCS, "MANIFEST.md")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("".join(out))
    print("manifest -> %s (%d files)" % (path, len(rows)))


if __name__ == "__main__":
    main()
