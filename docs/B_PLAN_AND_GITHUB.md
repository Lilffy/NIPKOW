# 尼普科夫鼓电视 · B 部分任务规划 + GitHub 协作指南

> 用途：把这份文件**整份喂给队友 A 的 DeepSeek**，它就能理解项目、按规范推进工作。
> 维护者：B（软件负责人）｜更新：2026-10-25
> 仓库：`https://github.com/<owner>/nipkow`（待建，建好后替换）

---

## 0. 给队友 AI 的说明（先读这段）

你是队友 A（硬件/机械负责人）的助手。你的职责：

1. **帮 A 完成硬件焊接、调试、机械装配、测试记录**，不要越界改软件架构
2. **所有工作以 GitHub Issue 为单位**推进，一个 issue 一件事，完成后附测试记录再关闭
3. **改硬件设计（原理图/PCB/BOM）前必须先问 B**，因为板子已经打样冻结，改动要走评审
4. 读代码/固件时只读不改；发现固件问题，开 issue 描述清楚，由 B 修
5. 不确定的地方**先问，不要猜**；涉及安全（上电、旋转、电机）必须先说明风险

先读这几个文件（按顺序）：
`README.md` → `docs/TASKS.md` → `docs/BOM.md` → `docs/SCHEMATIC_LAYOUT.md` → 本文件

---

## 1. 项目一页纸

**赛题**：第四届"嘉立创杯"南京理工大学新生电子设计竞赛 —— 柱状尼普科夫鼓机械扫描电视。

**原理**：Ø160×46 mm 的鼓，壁上 16 个小孔（1.255×1.961 mm）沿螺旋排布；鼓转一圈，16 个孔依次扫过 22.5° 固定视窗，每孔扫出一行 25 像素；RGB 灯按扫描时序调制颜色，人眼视觉暂留成 16×25 图像。

**关键指标**：

| 项 | 值 |
|---|---|
| 分辨率 | 16 行 × 25 列 = 400 像素 |
| 转速 | 1200 ± 20 rpm（加分 1800 rpm） |
| 帧率 | 20 fps（加分 30 fps） |
| 像素时间 | 125 µs（30fps 时 83.3 µs） |
| 视窗 | 22.5° / 弧长 31.4 mm |
| 供电 | 7.4–12 V（建议 9 V） |

**当前状态（2026-10-25）**：

- ✅ 原理图冻结（共阴 RGB：S8550 PNP 高边 + AO3400A 低边备用 DNP）
- ✅ PCB 完成：100×90 mm、2 层、59 器件、37 网络**全部布通**、DRC **0 错误**、底层 GND 铺铜
- ✅ 制造文件已导出：`docs/export/Gerber.zip`、`BOM.csv`、`PickAndPlace.csv`
- ⬜ 物料未到（电机/灯珠/传感器要等板子生产后）
- ⬜ 固件全部待开发（B 负责）

**核心板**：立创梁山派·天空星 STM32F407VET6（LQFP-100），双排 2×20 排针（共 80 脚）。

**关键引脚**（已冻结）：

| 功能 | 引脚 | 备注 |
|---|---|---|
| RGB R/G/B PWM | PA6 / PA7 / PB0 | TIM3 CH1/2/3，**开漏输出，PWM 极性取反** |
| 红外索引 | PA1 | EXTI1，下降沿（遮光时高电平） |
| 电机 PWM | PB6 | TIM4_CH1 |
| 按键 | PC0 / PC1 | 内部上拉，低有效 |
| 串口 | PA2 / PA3 | USART2，J7 排针（GND/TX/RX） |
| 板载用户 LED | PB2 | 低电平点亮（BOOT1 复用） |

---

## 2. 分工

| | A（硬件/机械） | B（软件） |
|---|---|---|
| 主要工作 | 焊接、上电测试、电气排查、机械装配、测试记录 | 固件全部、串口协议、上位机、扫描时序、失锁保护 |
| 交付物 | 焊接好的扩展板、机械组件、测试数据 | 可运行固件、演示程序、上位机工具 |
| 交接点 | 板子焊好 → 交给 B 下载固件；机械装好 → 联调 | 固件接口定义 → 交给 A 验证硬件 |

**接口约定**：

- A 焊接完成后，向 B 提供：各测试点电压（VIN/5V/3.3V）、索引信号波形、RGB 实际亮度/电流
- B 提供：`firmware/` 工程、烧录说明、串口指令表

---

## 3. B 部分任务规划（固件）

### 里程碑

| 里程碑 | 内容 | 验收标准 | 依赖 | 状态 |
|---|---|---|---|---|
| **M0 骨架** | 时钟 168 MHz、SysTick 延时、USART2 115200、PB2 心跳灯 | 串口打印版本号，LED 1 Hz 闪 | 核心板裸板 | ⬜ |
| **M1 红外 EXTI** | PA1 下降沿中断、20 ms 消抖、窄脉冲剔除、计数 | 遮光/移开各触发一次；中断后 LED 亮 1 s（非阻塞） | M0 + 扩展板 J4/J5 | ⬜ |
| **M2 RGB 调光** | TIM3 三通道 PWM（100 kHz 载频），开漏+极性取反，≥4 级亮度，8 色表 | 手电筒照灯珠能看到红/绿/蓝/黄/青/品红/白/黑 | M0 + 扩展板 J3 + 灯珠 | ⬜ |
| **M3 电机调速** | TIM4_CH1 PWM（频率/占空比按实物电调确认），启停/调速 | 电机能转、能停、能变速 | 电机+驱动 | ⬜ |
| **M4 串口协议** | `START/STOP/SET <rpm>/RGB <r> <g> <b>` 文本协议 | PC 串口助手可控制 | M0 | ⬜ |
| **M5 稳速闭环** | 索引周期测量（1 MHz 计数，滑动平均）、PI 调速、±20 rpm | 30 s 内转速稳定在 1200±20 | M1 + M3 + 机械 | ⬜ |
| **M6 整帧成像** | 帧缓冲 16×25、125 µs 像素时序、单行→整帧、8 色、切图、动画、失锁保护 | 静态图像 30 s 不漂移；≥2 幅切换；≥5 fps | M5 + 机械 | ⬜ |
| **M7 加分** | 灰度 ≥4 级、30 fps、PC 实时传图 | 按赛题加分项验收 | M6 | ⬜ |

### 代码结构（建议）

```
firmware/
├── common/            # 时钟、延时、串口、日志
├── drivers/           # led, ir_exti, rgb_pwm, motor_pwm, encoder
├── app/
│   ├── stage1/        # 第一阶段 5 个演示程序（可独立编译）
│   └── stage2/        # 扫描时序、帧缓冲、动画、失锁
└── tools/             # 上位机（Python 串口发图）
```

### 关键实现要点（写进 issue 的验收里）

1. **RGB 必须开漏输出**：PNP 发射极接 5V，推挽 3.3V 关不断；PWM 占空比取反
2. **红外中断不阻塞**：中断里只记时间戳/置标志，1 秒 LED 用 SysTick 或定时器非阻塞实现
3. **消抖**：两次边沿间隔 < 20 ms 判为抖动；连续两次周期差 > ±20% 判为干扰
4. **扫描时序**：`t = T/400`（T 为实测索引周期）；行号由孔序、列号由帧内计时
5. **切帧在索引中断里做**，避免撕裂
6. **失锁**：索引间隔 > 1.5T 立即熄灯、复位状态机

---

## 4. GitHub 进度管理

### 4.1 队友 A 首次配置（刚注册 GitHub，照做即可）

> 前提：网络能访问 GitHub。若在国内且没有代理，先开代理（下文有说明）。

**① 安装 Git for Windows**（已装可跳过）
- 下载：https://git-scm.com/download/win
- 安装时全部默认下一步即可

**② 配置身份**（在 PowerShell 里执行）

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的GitHub邮箱"
```

**③ 配置代理**（有"魔法"才需要；端口按你自己的代理软件改，常见 7890/7897）

```powershell
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897
```

如果 git 报 `schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS`：

```powershell
git config --global http.sslBackend openssl
```

验证代理是否生效：

```powershell
git ls-remote https://github.com/octocat/Hello-World.git
```

能列出 `HEAD` 就说明通了。

**④ 认证（二选一）**

- **方式一：GitHub CLI（推荐）**
  ```powershell
  winget install GitHub.cli
  gh auth login
  # 选：GitHub.com → HTTPS → Y（用浏览器登录）
  ```
- **方式二：Personal Access Token**
  1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
  2. 勾选 `repo`，设置 7 天过期，生成后复制
  3. 第一次 `git push` 时，用户名填 GitHub 用户名，**密码填 token**（Windows 会记住）

**⑤ 克隆仓库**

```powershell
cd D:\code          # 自己选一个目录
git clone https://github.com/<owner>/nipkow.git
cd nipkow
```

**⑥ 配置仓库内推送（只做一次）**

```powershell
git config user.name "你的名字"
git config user.email "你的邮箱"
git config http.sslBackend openssl
git config http.proxy http://127.0.0.1:7897
git config https.proxy http://127.0.0.1:7897
```

### 4.2 日常开发流程

```powershell
# 1) 先同步最新的 main
git pull origin main

# 2) 建自己的分支（A 用 feat/a-xxx，B 用 feat/b-xxx）
git checkout -b feat/a-hw-test

# 3) 改文件、加文件
git add -A

# 4) 提交（写明做了什么）
git commit -m "feat(hw): 完成扩展板电源焊接并记录 3.3V/5V 实测电压"

# 5) 推送
git push -u origin feat/a-hw-test
```

**提交信息规范**：

```
feat(hw): 新增内容      fix(hw): 修复问题
docs: 文档              test: 测试记录
feat(sw): 固件功能      wip: 未完成（允许，但别合 main）
```

**PR 流程**：
1. 网页打开仓库 → 会提示 "Compare & pull request"
2. 标题写清楚，描述里写：**改了什么 / 怎么验证的 / 影响范围**
3. 等 B 或队友 review 后合并
4. 不要在 main 上直接提交（除非只是改 README）

### 4.3 Issue 与看板（进度管理核心）

- 每个任务 = 一个 Issue，模板：

```
【目标】一句话
【验收】可测量的标准（电压/波形/现象）
【依赖】需要什么（物料/另一人的成果）
【记录】测试数据、截图、日志
```

- Label：`hw`（硬件）、`sw`（软件）、`test`（测试）、`bug`、`blocked`
- Projects 看板列：`Backlog → To Do → In Progress → Review → Done`
- 关闭 issue 前必须附**验收证据**（截图/万用表读数/波形照片）

### 4.4 常见错误排查

| 现象 | 原因 | 解决 |
|---|---|---|
| `schannel: SEC_E_NO_CREDENTIALS` | Windows TLS 后端问题 | `git config --global http.sslBackend openssl` |
| `Failed to connect github.com:443` | 网络被墙/代理没开 | 开代理；配 `http.proxy` |
| `Recv failure: Connection was reset` | 代理未生效或端口错 | 确认代理端口（设置→网络里看），重配 |
| `gh: 无法识别` | 没装 gh | `winget install GitHub.cli`，重开终端 |
| `remote: Permission denied` | 不是仓库协作者 | 让仓库主人在 Settings → Collaborators 邀请 |
| `! [rejected] non-fast-forward` | 远端有新提交 | 先 `git pull --rebase` 再 push |
| 冲突（CONFLICT） | 两人改了同一处 | 打开冲突文件，手动合并，`git add` 后 `git rebase --continue` |
| 大文件推不上去 | Gerber/PDF 太大 | 放 GitHub Releases，或用 Git LFS |

### 4.5 网络抽风时的兜底

- **优先用浏览器操作**：GitHub 网页能直接上传文件、在线改 README、建 issue/PR（走系统代理）
- **本地先提交**：`git commit` 不需要网络，网络恢复后再 `git push`
- **B 这边有 REST API 通道**：`api.github.com` 可用，必要时 B 可代传文件
- 如果连续失败：把完整报错发到群里，不要反复重试

---

## 5. 仓库结构（目标）

```
nipkow/
├── README.md              # 一页说明：项目、进度、怎么跑
├── docs/
│   ├── TASKS.md           # 任务清单（来源）
│   ├── B_PLAN.md          # 本文件
│   ├── BOM.md / BOM.csv
│   ├── SCHEMATIC_LAYOUT.md
│   ├── CHANGELOG.md
│   └── TEST_LOG.md        # A 的测试记录
├── hardware/
│   ├── Gerber.zip         # 制造文件（或放 Releases）
│   ├── PickAndPlace.csv
│   └── PCBInfo.txt
├── firmware/
│   ├── common/ drivers/ app/
│   └── README.md          # 烧录说明、串口指令表
└── tools/                 # 上位机、测试脚本
```

---

## 6. 测试记录模板（A 填写）

```markdown
## 测试记录 YYYY-MM-DD
- 板子编号：
- 测试项：电源上电
- 条件：输入 9.0 V，限流 300 mA
- 结果：VIN=9.00V, 5V=4.98V, 3V3=3.29V；U3 温度 42°C（无散热片）
- 波形/截图：<链接>
- 结论：通过 / 不通过（原因）
```

---

## 7. 给 AI 的协作约定

1. 每次只推进**一个 issue**，完成、附证据、关闭，再做下一个
2. 遇到硬件相关判断（能不能上电、线序、极性），先列风险再建议
3. 不确定的型号/参数**先问**，不要编造数据手册数值
4. 代码改动只在自己的分支，PR 里说明测试方法
5. 每周把 `docs/TASKS.md` 的勾选状态同步一次（或直接看 Projects 看板）
