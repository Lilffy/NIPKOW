# 把 LETTER_TO_B.md 推到 Lilffy/NIPKOW
#
# 用法：
#   1) 先开代理（Clash/V2Ray 等），确认端口
#   2) .\push_letter.ps1                      # 默认不开代理，走直连
#   3) .\push_letter.ps1 -Proxy 7897          # 走 127.0.0.1:7897
#   4) .\push_letter.ps1 -Proxy 7897 -SkipCheck
#
# 第一次 push 会弹 GitHub 登录窗口（浏览器），用 B 给你的协作者账号登录即可。
# 前提：你的 GitHub 账号已被 B 加为本仓库 Collaborator（Write 权限）。

param(
    [int]$Proxy = 0,
    [switch]$SkipCheck
)

$ErrorActionPreference = 'Stop'
$git = 'C:\Program Files\Git\cmd\git.exe'
$repo = Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) 'dist\nipkow'

if (-not (Test-Path $repo)) {
    Write-Host "找不到本地仓库：$repo" -ForegroundColor Red
    Write-Host "请先跑 tools/prepare_letter_repo.ps1" -ForegroundColor Yellow
    exit 1
}

# 1) TLS 后端：schannel 在这台机器上报 SEC_E_NO_CREDENTIALS，改用 openssl
& $git -C $repo config http.sslBackend openssl

# 2) 代理（可选）
if ($Proxy -gt 0) {
    & $git -C $repo config http.proxy "http://127.0.0.1:$Proxy"
    & $git -C $repo config https.proxy "http://127.0.0.1:$Proxy"
    Write-Host "已配置代理 127.0.0.1:$Proxy" -ForegroundColor Cyan
} else {
    & $git -C $repo config --unset http.proxy  2>$null
    & $git -C $repo config --unset https.proxy 2>$null
}

# 3) 连通性检查（读）
if (-not $SkipCheck) {
    Write-Host "检查 GitHub 连通性 ..." -NoNewline
    $env:GIT_TERMINAL_PROMPT = '0'
    $probe = & $git -c http.sslBackend=openssl ls-remote https://github.com/Lilffy/NIPKOW.git 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        Write-Host " 失败" -ForegroundColor Red
        Write-Host $probe.Trim() -ForegroundColor DarkGray
        Write-Host "`n网络没通。试试 -Proxy <端口>，或先开代理再跑。" -ForegroundColor Yellow
        exit 2
    }
    Write-Host " OK" -ForegroundColor Green
}

# 4) 推送（会弹登录窗）
Write-Host "`n推送中 ...（第一次会打开浏览器让你登录 GitHub）" -ForegroundColor Cyan
$env:GIT_TERMINAL_PROMPT = '1'
& $git -C $repo push -u origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n成功：https://github.com/Lilffy/NIPKOW/blob/main/LETTER_TO_B.md" -ForegroundColor Green
} else {
    Write-Host "`n推送失败。" -ForegroundColor Red
    Write-Host "常见原因：" -ForegroundColor Yellow
    Write-Host "  · 没有 Collaborator 权限 → 让 B 在 Settings → Collaborators 加你"
    Write-Host "  · 网络被重置 → 加 -Proxy <端口> 再试"
    Write-Host "  · 登录窗口没弹 → 手动跑：git -C `"$repo`" push -u origin main"
}
