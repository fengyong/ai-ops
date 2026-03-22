# WSL 离线安装脚本
# 使用说明:
# 1. 下载 Ubuntu 镜像（选择一个可用的源）:
#    方法 1: 微软应用商店（推荐）
#      - 打开 Microsoft Store
#      - 搜索 "Ubuntu 22.04"
#      - 点击获取/安装
#      - 安装完成后，镜像位于：%LOCALAPPDATA%\Packages\CanonicalGroupLimited.Ubuntu2204...
#    
#    方法 2: 从 GitHub 下载官方镜像
#      https://github.com/microsoft/WSL/releases
#      下载 Ubuntu-22.04.appx 或 .msixbundle
#    
#    方法 3: 使用 wsl --install 在线安装（较慢但简单）
#      wsl --install -d Ubuntu-22.04
#
# 2. 以管理员身份运行此脚本

param(
    [string]$DownloadFilePath = "",
    [string]$WSLInstallPath = "D:\WSL\Ubuntu2204",
    [string]$DistributionName = "Ubuntu-22.04"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   WSL 离线安装脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "错误：请以管理员身份运行此脚本" -ForegroundColor Red
    Write-Host "右键点击脚本 -> '以管理员身份运行'" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/6] 检查 WSL 状态..." -ForegroundColor Green

try {
    $wslStatus = wsl --list --quiet 2>$null
    $wslAvailable = ($LASTEXITCODE -eq 0)
} catch {
    $wslAvailable = $false
}

if (-not $wslAvailable) {
    Write-Host "WSL 未启用，正在启用 WSL 功能..." -ForegroundColor Yellow
    
    # 尝试使用 wsl --install --no-distribution
    Write-Host "执行：wsl --install --no-distribution" -ForegroundColor Gray
    try {
        wsl --install --no-distribution
        $wslInstallSuccess = ($LASTEXITCODE -eq 0)
    } catch {
        $wslInstallSuccess = $false
    }
    
    if (-not $wslInstallSuccess) {
        Write-Host "使用 DISM 启用 WSL 功能..." -ForegroundColor Yellow
        dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
        
        Write-Host "启用虚拟机平台功能（WSL 2 需要）..." -ForegroundColor Yellow
        dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
        
        Write-Host "`n重要：需要重启电脑后才能继续安装" -ForegroundColor Yellow
        Write-Host "请重启电脑后重新运行此脚本" -ForegroundColor Cyan
        exit 0
    }
} else {
    Write-Host "WSL 已启用" -ForegroundColor Green
}

Write-Host "`n[2/6] 检查下载文件..." -ForegroundColor Green

# 如果没有指定下载路径，尝试自动查找
if ([string]::IsNullOrWhiteSpace($DownloadFilePath)) {
    Write-Host "未指定下载路径，尝试自动查找 Ubuntu 镜像..." -ForegroundColor Yellow
    
    # 在常见位置查找 .appx 或 .msixbundle 文件
    $possiblePaths = @(
        "$env:USERPROFILE\Downloads",
        "$env:LOCALAPPDATA\Packages",
        "$env:TEMP"
    )
    
    foreach ($basePath in $possiblePaths) {
        if (Test-Path $basePath) {
            $files = Get-ChildItem -Path $basePath -Filter "*ubuntu*.appx" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($files) {
                $DownloadFilePath = $files.FullName
                Write-Host "找到镜像文件：$DownloadFilePath" -ForegroundColor Green
                break
            }
        }
    }
    
    if ([string]::IsNullOrWhiteSpace($DownloadFilePath)) {
        Write-Host "错误：找不到 Ubuntu 镜像文件" -ForegroundColor Red
        Write-Host "`n请选择以下任一方式:" -ForegroundColor Yellow
        Write-Host "1. 从微软应用商店安装 'Ubuntu 22.04'，然后重新运行此脚本" -ForegroundColor White
        Write-Host "2. 从 GitHub 下载：https://github.com/microsoft/WSL/releases" -ForegroundColor White
        Write-Host "3. 直接使用命令安装：wsl --install -d Ubuntu-22.04" -ForegroundColor White
        Write-Host "`n或者指定镜像路径运行此脚本:" -ForegroundColor White
        Write-Host ".\install-wsl.ps1 -DownloadFilePath 'C:\path\to\ubuntu-22.04.appx'" -ForegroundColor Cyan
        exit 1
    }
} else {
    # 验证指定的路径
    if (-not (Test-Path $DownloadFilePath)) {
        Write-Host "错误：指定的镜像文件不存在" -ForegroundColor Red
        Write-Host "路径：$DownloadFilePath" -ForegroundColor Gray
        Write-Host "`n请检查路径是否正确" -ForegroundColor Yellow
        exit 1
    } else {
        Write-Host "找到下载文件：$DownloadFilePath" -ForegroundColor Green
    }
}

Write-Host "`n[3/6] 创建 WSL 安装目录..." -ForegroundColor Green
if (-not (Test-Path $WSLInstallPath)) {
    New-Item -ItemType Directory -Path $WSLInstallPath -Force | Out-Null
    Write-Host "已创建目录：$WSLInstallPath" -ForegroundColor Green
} else {
    Write-Host "目录已存在：$WSLInstallPath" -ForegroundColor Yellow
}

Write-Host "`n[4/6] 导入 WSL 发行版..." -ForegroundColor Green

# 先注销已存在的同名发行版（如果存在）
try {
    $existingDistros = wsl --list --quiet 2>$null
    if ($existingDistros -match $DistributionName) {
        Write-Host "检测到同名发行版，正在注销..." -ForegroundColor Yellow
        wsl --unregister $DistributionName
    }
} catch {
    Write-Host "无法检查现有发行版，继续执行..." -ForegroundColor Yellow
}

# 导入新的发行版
Write-Host "正在从 $DownloadFilePath 导入到 $WSLInstallPath" -ForegroundColor Gray
try {
    wsl --import $DistributionName $WSLInstallPath $DownloadFilePath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ WSL 发行版导入成功" -ForegroundColor Green
    } else {
        Write-Host "✗ WSL 发行版导入失败" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ 导入过程中发生错误" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host "`n[5/6] 配置 WSL 版本..." -ForegroundColor Green

# 设置为 WSL 2
Write-Host "设置 WSL 版本为 2..." -ForegroundColor Gray
try {
    wsl --set-version $DistributionName 2
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 已设置为 WSL 2 版本" -ForegroundColor Green
    } else {
        Write-Host "⚠ 设置 WSL 版本失败，但不影响使用" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ 设置 WSL 版本时出错" -ForegroundColor Yellow
}

# 设置为默认发行版
Write-Host "设置为默认发行版..." -ForegroundColor Gray
try {
    wsl --set-default $DistributionName
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 已设置为默认发行版" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ 设置默认发行版失败" -ForegroundColor Yellow
}

Write-Host "`n[6/6] 验证安装..." -ForegroundColor Green
Write-Host "已安装的 WSL 发行版:" -ForegroundColor Gray
try {
    wsl --list --verbose
} catch {
    Write-Host "无法列出 WSL 发行版" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   WSL 安装完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor Yellow
Write-Host "1. 运行 'wsl' 或 'wsl -d $DistributionName' 启动 Ubuntu" -ForegroundColor White
Write-Host "2. 首次启动需要设置用户名和密码" -ForegroundColor White
Write-Host "3. 运行配置脚本完成开发环境设置" -ForegroundColor White
Write-Host ""
