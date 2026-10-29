# -*- coding: utf-8 -*-
"""
生成「需自购元器件」清单 + 立创商城可导入的 BOM 文件。

依据：
  - 赛题表 1（主办方提供）：无锁按键 C5379898 / 自锁按键 C2693640 / 0603 阻容 /
    可调 LDO TO-220 C498319 / 3.3V LDO SOT-223 C126027 / 排针 / 核心板 C22370035 / RGB 灯珠
  - B 的 hardware/BOM.csv（59 器件，立创编号）

输出：
  docs/purchase/采购清单.md
  docs/purchase/采购清单.csv          （人看，带位号/规格/编号）
  docs/purchase/立创BOM导入.csv        （EasyEDA BOM 列格式，直接上传立创「BOM 配单」）
"""

import csv
import os

WS = r"C:\旋转电视"
OUT = os.path.join(WS, "docs", "purchase")
os.makedirs(OUT, exist_ok=True)

# (位号, 名称, 规格, 封装, 数量, 立创编号, 备注)
BUY = [
    ("D1", "肖特基二极管", "SS34 40V/3A", "SMA", 2, "C7420365", "防反接；多买1个备损"),
    ("D2", "贴片 LED", "GL0603UG01 绿色", "0603", 2, "C51933293", "电源指示；多买1个"),
    ("Q4,Q5,Q6", "PNP 三极管", "S8550，丝印 2TY", "SOT-23", 5, "C20069126",
     "RGB 高边；**丝印必须是 2TY**（J3Y 是 S8050，买错全不亮）；多买2个"),
    ("H1,H2", "排母 2×20", "2.54mm 双排母 40P 方孔", "插件", 2, "C53202170",
     "**主办方只提供排针，不提供排母**；老编号 C50982 已停售"),
    ("J1", "电源接线端子", "XY301V-A-5.0-2P（5.0mm）", "插件", 1, "C9900016950", "9V 输入"),
    ("J3", "XH2.54 插座", "A2547WV-4P 立式", "插件", 2, "C9900216472", "RGB 灯珠；多买1个"),
    ("J4,J5,J6,J7", "排针 1×2 / 1×5 / 1×4", "由提供的 1×40 排针掰断", "插件", 0, "—",
     "**不用买**：赛题提供 2.54 排针，按需掰断即可（J6 想要带扣的可另买 MDF7-5P C19088617）"),
    ("JP1", "短路帽", "2.54mm 跳线帽（排针用提供的）", "插件", 3, "C100114", "5V 注入核心板；多买2个"),
    ("TP1–TP9", "测试针", "RH-5000 Ø1.4", "插件", 9, "C5277086", "板边测试点"),
    ("C-EXT", "铝电解电容", "100µF/25V（≥16V）", "直插 6.3×7.7", 2, "C72477",
     "**C10 已改 10µF，这颗必须外接**到 J1 或 J6 电源端；多买1个"),
    ("SW1", "总电源开关", "SS12D10G5 滑动开关（老师群里指定）", "插件", 2, "C7431054",
     "2A/125V 单刀双掷；串在 9V 电源线正极（COM→9V，NO→J1-1）；板已下单装不到板上"),
    ("—", "散热片", "TO-220 铝 10×10×8（B 建议；15×15×10 也行）", "—", 1, "—",
     "U3 必装；**另配绝缘垫片+绝缘粒**（TO-220 背板是 5V，不是 GND）+ 导热硅脂"),
    ("—", "M3 铜柱", "M3×10 六角双通", "—", 4, "C551330", "配 4 个安装孔"),
    ("—", "M3 螺丝+螺母", "M3×8 盘头+螺母+垫片", "—", 8, "—", "不锈钢"),
    ("Q1–Q3", "N-MOS", "AO3400A", "SOT-23", 0, "C700953", "**DNP 不贴，不用买**"),
]

# 主办方给的是"0603 阻容一套"，但具体阻值/容值不一定全，缺的按这个补
SPARE = [
    ("R3", "180Ω 1% 1/10W", "0603", 5, "C22828"),
    ("R6,R9,R10", "120Ω 1% 1/10W", "0603", 5, "C22787"),
    ("R11", "360Ω 1% 1/10W", "0603", 5, "待查证"),
    ("R12", "220Ω 1% 1/10W（B 建议，200 也可）", "0603", 5, "待查证"),
    ("R13,R14,R17–R19", "1kΩ 1% 1/10W", "0603", 10, "C21190"),
    ("R2,R5,R8,R15,R20–R22", "10kΩ 1% 1/10W", "0603", 10, "C25804"),
    ("R16", "470Ω 1% 1/10W", "0603", 5, "C23179"),
    ("R23", "0Ω 1/10W", "0603", 5, "C21189"),
    ("C1–C4", "10µF/16V X5R", "0603", 10, "C19702"),
    ("C5–C9", "100nF/50V X7R", "0603", 10, "C1591"),
    ("C10", "10µF/25V X5R", "0603", 5, "待查证"),
]

PROVIDED = [
    ("核心板", "STM32F407VET6 天空星", "C22370035"),
    ("3.3V LDO", "LM1117-3.3，SOT-223", "C126027"),
    ("可调 LDO", "TO-220，5V 输出", "C498319"),
    ("无锁按键 ×2", "5.8×5.8 六脚 DPDT 插件", "C5379898"),
    ("自锁按键", "插件", "C2693640"),
    ("排针", "2.54mm 直针，1×40 可掰", "通用"),
    ("0603 电阻 / 电容", "贴片阻容一套", "通用"),
    ("RGB 灯珠", "8mm 4 针，焊线安装", "提供"),
]


def _open_out(path):
    """文件被 Excel/预览占用时，自动另存为 *_新.csv"""
    try:
        return open(path, "w", encoding="utf-8-sig", newline=""), path
    except PermissionError:
        alt = path.rsplit(".", 1)[0] + "_新.csv"
        print("[警告] %s 被占用，改写到 %s" % (path, alt))
        return open(alt, "w", encoding="utf-8-sig", newline=""), alt


def main():
    # ---------- 立创 BOM 导入（EasyEDA 列格式，UTF-8 BOM 便于 Excel 打开） ----------
    bom_path = os.path.join(OUT, "立创BOM导入.csv")
    f, bom_path = _open_out(bom_path)
    with f:
        w = csv.writer(f)
        w.writerow(["No.", "Quantity", "Comment", "Designator", "Footprint", "Value",
                    "Manufacturer Part", "Manufacturer", "Supplier Part", "Supplier"])
        i = 0
        for ref, name, spec, pkg, qty, lcsc, note in BUY:
            if qty <= 0 or lcsc == "—":
                continue
            i += 1
            w.writerow([i, qty, name, ref, pkg, spec, "", "", lcsc, "LCSC"])

    print("bom ->", bom_path, "行数", i)

    # 可选补购阻容（单独文件，别和主 BOM 一起上传，避免行数多、剪带费高）
    spare_path = os.path.join(OUT, "可选补购阻容.csv")
    f, spare_path = _open_out(spare_path)
    with f:
        w = csv.writer(f)
        w.writerow(["No.", "Quantity", "Comment", "Designator", "Footprint", "Value",
                    "Manufacturer Part", "Manufacturer", "Supplier Part", "Supplier"])
        for k, (ref, spec, pkg, qty, lcsc) in enumerate(SPARE, 1):
            val = spec.replace("**", "")
            lc = "" if lcsc.startswith("待") else lcsc
            w.writerow([k, qty, val.split(" ")[0], ref, pkg, val, "", "", lc,
                        "LCSC" if lc else ""])
    print("spare ->", spare_path)

    # ---------- 人看版 CSV ----------
    list_path = os.path.join(OUT, "采购清单.csv")
    f, list_path = _open_out(list_path)
    with f:
        w = csv.writer(f)
        w.writerow(["位号", "名称", "规格", "封装", "数量", "立创编号", "备注"])
        for row in BUY:
            w.writerow(row)
    print("list ->", list_path)

    # ---------- Markdown ----------
    md = []
    md.append("# 需自购元器件清单（已剔除主办方提供件）\n")
    md.append("> 依据：赛题表 1 + B 的 `hardware/BOM.csv`（59 器件）")
    md.append("> 生成：`.tools/make_purchase_list.py`　更新：2026-10-27\n")
    md.append("## 0. 为什么清单这么短\n")
    md.append("赛题表 1 已经提供了一整套主要元器件，**阻容、排针、两个 LDO、按键、核心板、RGB 灯珠都不用买**。")
    md.append("真正要自己买的只有 7 类东西 + 补购几个阻值。\n")
    md.append("| 主办方提供（不用买） | 编号 |")
    md.append("|---|---|")
    for name, spec, code in PROVIDED:
        md.append("| %s（%s） | %s |" % (name, spec, code))
    md.append("")
    md.append("## 1. 必须买（有立创编号，可直接下单）\n")
    md.append("| 位号 | 器件 | 规格 | 封装 | 数量 | 立创编号 | 备注 |")
    md.append("|---|---|---|---|---:|---|---|")
    for ref, name, spec, pkg, qty, lcsc, note in BUY:
        if qty <= 0:
            md.append("| %s | %s | %s | %s | 0 | %s | %s |" % (ref, name, spec, pkg, lcsc, note))
            continue
        md.append("| %s | %s | %s | %s | %d | **%s** | %s |" % (ref, name, spec, pkg, qty, lcsc, note))
    md.append("")
    md.append("## 2. 建议补购的阻容（主办方给的套装不一定有这些值）\n")
    md.append("| 位号 | 规格 | 封装 | 建议数量 | 立创编号 |")
    md.append("|---|---|---|---:|---|")
    for ref, spec, pkg, qty, lcsc in SPARE:
        md.append("| %s | %s | %s | %d | %s |" % (ref, spec, pkg, qty, lcsc))
    md.append("")
    md.append("## 3. 三个容易买错的地方\n")
    md.append("1. **S8550 丝印必须是 `2TY`**。`J3Y` 是 S8050（NPN），装上去三路 RGB 全不亮。")
    md.append("2. **排母要自己买**。赛题只提供「排针」，核心板是插在**排母**上的，2×20 双排 ×2。")
    md.append("3. **C10 只买 10µF/25V 0603**，100µF 是外接的电解（直插），别指望贴 0603。")
    md.append("")
    md.append("## 4. 工具（如果没有，需要借或买）\n")
    md.append("| 工具 | 用途 | 备注 |")
    md.append("|---|---|---|")
    md.append("| 可调温电烙铁（350°C，尖头） | 焊接 | 配合 0.8mm 含松香焊锡 |")
    md.append("| 助焊剂 | 焊点发亮 | 比焊锡更关键 |")
    md.append("| 吸锡带 3mm | 拆件/清连锡 | |")
    md.append("| 尖头镊子 | 夹 0603 | |")
    md.append("| 万用表 | 通断/电压/二极管 | A 最重要的工具 |")
    md.append("| **可调限流电源** | 第一次上电 | **必须**，实验室借 |")
    md.append("| 示波器 | 看 PWM/红外波形 | 实验室借 |")
    md.append("")
    md.append("## 4.4 总电源开关（2026-10-29 老师通知）\n")
    md.append("刘学敏老师在群里通知：**C7431054**，大家在总电源也加一个开关。\n")
    md.append("| 项 | 内容 |")
    md.append("|---|---|")
    md.append("| 器件 | SS12D10G5 滑动开关（首韩 SHOU HAN），**C7431054** |")
    md.append("| 参数 | **额定 2A / 125V**，单刀双掷（SPDT），直插，12.7×6.7×11.2mm，寿命 3000 次 |")
    md.append("| 装哪里 | **串在 9V 电源线正极上**（适配器 → 开关 → J1-1）。板子已下单，来不及改板 |")
    md.append("| 买几个 | 2（1 用 1 备） |")
    md.append("| 备选 | 库存 0 时可买 **KCD1-101 船型开关 6A/250V**（淘宝 1–2 元），电流余量更大 |")
    md.append("")
    md.append("**电流校核（按实测参数 2A 算）**：")
    md.append("- 平时：5V 负载（核心板 ~120mA + RGB 45mA + 红外 20mA）≈ 0.9W → 9V 输入侧 ≈ **0.1A**")
    md.append("- 加电机：3720 空载 0.1–0.3A、带鼓 0.3–0.8A、启动/堵转 1–2A")
    md.append("- 合计：平时 **0.2–0.9A**，峰值 **1–2A** → **2A 开关够用（平时余量 2–10 倍，峰值刚好卡额定）**")
    md.append("")
    md.append("⚠️ 但注意两点：")
    md.append("1. **电机是感性负载**，启动瞬间有浪涌，工程上对 2A 开关建议按 1–1.5A 连续使用。所以**电机别带鼓启动**，先空载试。")
    md.append("2. **单刀双掷（SPDT）只有常开/常闭两组**：中间脚（COM）接 9V 进，任选一个边脚接 J1-1，第三个脚空着。")
    md.append("")
    md.append("> 备选：如果实测堵转 >2A（比如电机比预期猛），换 KCD1-101 船型开关（6A/250V，1–2 元）。\n")
    md.append("## 4.5 MOQ（最小起订量）怎么处理\n")
    md.append("**MOQ = Minimum Order Quantity，最小起订量**。商城标「5 起订、5 递增」，意思是至少买 5 个、且只能按 5 的倍数加。\n")
    md.append("记忆口诀：**便宜的多买，贵的按需**。一只几分钱的阻容买 100 只不亏；一只 1 元的铜柱买 100 只就是浪费。\n")
    md.append("| 物料 | 板上要用 | 建议下单 | 理由 |")
    md.append("|---|---:|---:|---|")
    md.append("| SS34 / S8550 / LED 0603 | 2 / 3 / 1 | 各 10 | 单价几毛，焊坏/烧了有备件 |")
    md.append("| 排母 2×20 | 2 | 2（MOQ 5 就买 5） | 必备件，多 3 个不心疼 |")
    md.append("| 电源端子 / XH2.54 | 1 / 1 | 各 2 | 塑料件容易烫变形 |")
    md.append("| 100µF 电解 | 1 | 2 | 极性装反会爆，留一个 |")
    md.append("| 短路帽 | 1 | 10 | 极小件，掉了找不到，淘宝更便宜 |")
    md.append("| 测试针 RH-5000 | 9 | 10 | 若 MOQ 100，**改去淘宝买 10 个** |")
    md.append("| M3 铜柱 + 螺丝 | 4 + 8 | 淘宝买套装 | 立创常 100 起订，淘宝 20 个一套 |")
    md.append("| 散热片 | 1 | 2 | 淘宝按尺寸买，几块钱 |")
    md.append("")
    md.append("**分两条渠道买最省**：")
    md.append("- **立创商城**：芯片/三极管/二极管/排母/端子（要正品、要对编号）")
    md.append("- **淘宝**：测试针、铜柱螺丝、短路帽、散热片（数量灵活、几块钱包邮）")
    md.append("")
    md.append("## 4.6 为什么料钱很便宜、总价却高\n")
    md.append("按可能性从高到低排查：\n")
    md.append("| # | 费用项 | 典型金额 | 怎么避免 |")
    md.append("|---|---|---|---|")
    md.append("| 1 | **走了 SMT 贴片流程**（工程费/钢网费/备料服务费） | 一单几十到上百 | 你们手焊，**只买料，不走贴片** |")
    md.append("| 2 | **运费**（立创未满额要运费） | 10–20 元 | 凑单到免邮门槛，或选到付/自提 |")
    md.append("| 3 | **MOQ 倍数**：某料 100 起订，你填 2 套 → 变 200 只 | 视物料 | 逐行看数量，把 100 只的件挑出来 |")
    md.append("| 4 | **Cut Tape（剪带）服务费** | 几元/种 | 选整卷或接受剪带费（小单常见） |")
    md.append("| 5 | **整盘/最小包装**：BOM 匹配成整盘 | 几十到上百 | 手动改成按只买 |")
    md.append("")
    md.append("**怎么一眼看出是哪一项**：在购物车/结算页找「费用明细」或「小计」列，")
    md.append("按小计从大到小排序——排第一的那行就是元凶（通常是某个 100 只的件或整盘价）。\n")
    md.append("## 5. 怎么直接导入立创商城\n")
    md.append("### 5.1 上传后弹出的「贴片数量」怎么填\n")
    md.append("那是**你要做几块板（套数）**，不是元器件个数，也不是你买几颗电阻。\n")
    md.append("- 系统会按「BOM 里每块板的用量 × 这个数量」帮你算总需求（含损耗）")
    md.append("- 你们自己手焊、总共只要 1 块板 → **选 2**（最少就是 2 套）")
    md.append("- 想多点备损（手焊容易焊坏）→ 选 5，但成本翻倍，不太值")
    md.append("- 「其他数量」= 自定义套数，同样最少 2；填 3、8 都行\n")
    md.append("> 只是买料、不需要他们贴片的话，用「BOM 配单」直接加购物车就行，不用选贴片数量。\n")
    md.append("### 5.2 BOM 配单在哪\n")
    md.append("**直接打开：https://bom.szlcsc.com/** （立创BOM智能云表）\n")
    md.append("或者：立创商城首页 <https://www.szlcsc.com/> 顶部导航，在「PLUS会员」右边就是「**BOM配单**」。\n")
    md.append("> ⚠️ 注意区分：你截图里的「BOM备料 / BOM整单订单 + 贴片数量」是 **嘉立创 SMT**（jlc-smt.com）的流程，")
    md.append("> 那是把元件备给贴片厂用的，**手焊不需要**。买元件去商城，不要走 SMT 那条线。\n")
    md.append("**最省事的备选**：不用 BOM 工具，直接在商城搜索框输入 C 编号（如 `C7420365`）→ 商品页 → 加入购物车，")
    md.append("11 个料点 11 次，5 分钟搞定，还不会匹配错。\n")
    md.append("### 5.3 步骤\n")
    md.append("1. 打开嘉立创/立创商城 → 搜「**BOM 配单**」（或 szlcsc.com/bom）")
    md.append("2. 上传 `docs/purchase/立创BOM导入.csv`")
    md.append("3. 它会按 `Supplier Part`（C 编号）自动匹配商品；**没有 C 编号的阻容会显示未匹配**，手动搜值补上即可")
    md.append("4. 核对数量，加入购物车\n")
    md.append("> 如果它不认列名：把表头改成 `位号,数量,型号,封装`，或者直接用 `采购清单.csv` 手工搜。\n")
    md.append("## 6. 变更记录\n")
    md.append("| 日期 | 内容 |")
    md.append("|---|---|")
    md.append("| 2026-10-27 | 首版：按赛题表 1 剔除提供件，剩 7 类 + 补购阻容 |")

    md_path = os.path.join(OUT, "采购清单.md")
    with open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(md))
    print("md   ->", md_path)


if __name__ == "__main__":
    main()
