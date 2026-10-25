# 编译固件（M0+）：优先用 CMake，失败则提示
# 用法：powershell -ExecutionPolicy Bypass -File tools/build.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$fw = Join-Path $root "firmware"

# 1) 工具链：优先环境变量，其次常见路径
$gccDir = $env:ARM_GCC_DIR
if (-not $gccDir) {
    $guess = Get-ChildItem "C:\Users\$env:USERNAME\Downloads" -Directory -Filter "arm-gnu-toolchain-*" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($guess) { $gccDir = $guess.FullName }
}
if (-not $gccDir) { throw "找不到 arm-none-eabi-gcc，请设置 ARM_GCC_DIR 或把工具链 bin 加入 PATH" }
$env:Path = (Join-Path $gccDir "bin") + ";" + $env:Path

# 2) CMake / Ninja：优先仓库自带
$cmake = Get-Command cmake -ErrorAction SilentlyContinue
if (-not $cmake) {
    $c = Get-ChildItem (Join-Path $root ".tools\bin\cmake") -Recurse -Filter cmake.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($c) { $cmake = $c.FullName; $env:Path = (Split-Path $c.FullName) + ";" + $env:Path }
}
$ninja = Get-Command ninja -ErrorAction SilentlyContinue
if (-not $ninja) {
    $n = Get-ChildItem (Join-Path $root ".tools\bin\ninja") -Recurse -Filter ninja.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($n) { $ninja = $n.FullName; $env:Path = (Split-Path $n.FullName) + ";" + $env:Path }
}

if (-not $cmake) { throw "找不到 cmake：winget install Kitware.CMake，或把 cmake.exe 放到 PATH" }

Write-Host "== CMake: $cmake"
Write-Host "== GCC:   $((Get-Command arm-none-eabi-gcc).Source)"

Push-Location $fw
try {
    if (-not (Test-Path "build")) {
        & $cmake -B build -G Ninja
        if ($LASTEXITCODE -ne 0) { throw "cmake configure 失败" }
    }
    & $cmake --build build
    if ($LASTEXITCODE -ne 0) { throw "编译失败" }
    $elf = Get-ChildItem "build" -Filter *.elf | Select-Object -First 1
    if ($elf) {
        Write-Host "`n== 产物: $($elf.FullName)"
        & arm-none-eabi-size $elf.FullName
    }
} finally {
    Pop-Location
}
