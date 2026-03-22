# WSL 验证脚本
# 用于验证 WSL 安装是否正常工作

param(
    [string]$DistributionName = "Ubuntu2204"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   WSL 验证测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 测试 1: 检查 WSL 是否已安装
Write-Host "[1/7] 检查 WSL 安装状态..." -ForegroundColor Green
$wslVersion = wsl --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ WSL 已安装" -ForegroundColor Green
    Write-Host "版本信息:" -ForegroundColor Gray
    Write-Host $wslVersion -ForegroundColor Gray
} else {
    Write-Host "✗ WSL 未安装或无法访问" -ForegroundColor Red
    exit 1
}

# 测试 2: 检查发行版列表
Write-Host "`n[2/7] 检查已安装的发行版..." -ForegroundColor Green
$distros = wsl --list --verbose
Write-Host $distros -ForegroundColor Gray

if ($distros -match $DistributionName) {
    Write-Host "✓ 找到发行版：$DistributionName" -ForegroundColor Green
} else {
    Write-Host "⚠ 未找到发行版：$DistributionName" -ForegroundColor Yellow
}

# 测试 3: 检查 WSL 版本
Write-Host "`n[3/7] 检查 WSL 版本..." -ForegroundColor Green
$versionInfo = wsl --status
Write-Host $versionInfo -ForegroundColor Gray

# 测试 4: 启动 WSL 并执行基本命令
Write-Host "`n[4/7] 测试 WSL 启动和基本命令..." -ForegroundColor Green
$testOutput = wsl -d $DistributionName -- echo "WSL 测试成功"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ WSL 启动成功" -ForegroundColor Green
    Write-Host "输出：$testOutput" -ForegroundColor Gray
} else {
    Write-Host "✗ WSL 启动失败" -ForegroundColor Red
}

# 测试 5: 检查网络连接
Write-Host "`n[5/7] 测试网络连接..." -ForegroundColor Green
$networkTest = wsl -d $DistributionName -- bash -c "ping -c 1 8.8.8.8 > /dev/null && echo '网络正常' || echo '网络异常'"
Write-Host $networkTest -ForegroundColor Gray

# 测试 6: 检查文件系统
Write-Host "`n[6/7] 测试文件系统..." -ForegroundColor Green
$fsTest = wsl -d $DistributionName -- bash -c "df -h / | tail -1"
Write-Host $fsTest -ForegroundColor Gray

# 测试 7: 检查系统信息
Write-Host "`n[7/7] 获取系统信息..." -ForegroundColor Green
$sysInfo = wsl -d $DistributionName -- bash -c "uname -a"
Write-Host $sysInfo -ForegroundColor Gray

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   验证完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "如果所有测试通过，WSL 可以正常使用" -ForegroundColor White
Write-Host ""
Write-Host "常用命令:" -ForegroundColor Yellow
Write-Host "  wsl                          # 启动默认发行版" -ForegroundColor White
Write-Host "  wsl -d $DistributionName     # 启动指定发行版" -ForegroundColor White
Write-Host "  wsl --shutdown              # 关闭所有 WSL 实例" -ForegroundColor White
Write-Host "  wsl --list --verbose        # 查看发行版列表" -ForegroundColor White
Write-Host ""
