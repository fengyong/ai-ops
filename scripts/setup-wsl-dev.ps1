# WSL 开发环境配置脚本
# 用于安装常用的开发工具和依赖

param(
    [string]$DistributionName = "Ubuntu2204"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   WSL 开发环境配置" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "此脚本将安装以下工具:" -ForegroundColor Yellow
Write-Host "  - Git" -ForegroundColor White
Write-Host "  - Python3 + pip" -ForegroundColor White
Write-Host "  - Node.js + npm" -ForegroundColor White
Write-Host "  - Docker (可选)" -ForegroundColor White
Write-Host "  - 常用开发工具 (curl, wget, vim, etc.)" -ForegroundColor White
Write-Host ""

$continue = Read-Host "是否继续安装？(y/n)"
if ($continue -ne 'y' -and $continue -ne 'Y') {
    Write-Host "已取消安装" -ForegroundColor Yellow
    exit 0
}

Write-Host "`n[1/6] 更新软件包列表..." -ForegroundColor Green
wsl -d $DistributionName -- sudo apt update

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ 更新失败，但继续执行..." -ForegroundColor Yellow
}

Write-Host "`n[2/6] 安装基础开发工具..." -ForegroundColor Green
$basicTools = "git,curl,wget,vim,net-tools,iputils-ping,software-properties-common,apt-transport-https,ca-certificates,gnupg,lsof"
wsl -d $DistributionName -- sudo apt install -y $basicTools

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 基础工具安装完成" -ForegroundColor Green
} else {
    Write-Host "⚠ 部分工具安装失败" -ForegroundColor Yellow
}

Write-Host "`n[3/6] 安装 Python3 和 pip..." -ForegroundColor Green
wsl -d $DistributionName -- sudo apt install -y python3 python3-pip python3-venv python3-dev

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python3 安装完成" -ForegroundColor Green
    
    # 验证 Python 版本
    $pythonVersion = wsl -d $DistributionName -- python3 --version
    Write-Host $pythonVersion -ForegroundColor Gray
} else {
    Write-Host "⚠ Python3 安装失败" -ForegroundColor Yellow
}

Write-Host "`n[4/6] 安装 Node.js 和 npm..." -ForegroundColor Green
# 使用 NodeSource 仓库安装较新版本的 Node.js
wsl -d $DistributionName -- bash -c "curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
wsl -d $DistributionName -- sudo apt install -y nodejs

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Node.js 安装完成" -ForegroundColor Green
    
    # 验证版本
    $nodeVersion = wsl -d $DistributionName -- node --version
    $npmVersion = wsl -d $DistributionName -- npm --version
    Write-Host $nodeVersion -ForegroundColor Gray
    Write-Host "npm $npmVersion" -ForegroundColor Gray
} else {
    Write-Host "⚠ Node.js 安装失败" -ForegroundColor Yellow
    Write-Host "可以尝试手动安装：" -ForegroundColor Gray
    Write-Host "wsl -d $DistributionName -- sudo apt install -y nodejs npm" -ForegroundColor Gray
}

Write-Host "`n[5/6] 安装 Docker (可选)..." -ForegroundColor Green
$dockerInstall = Read-Host "是否安装 Docker? (y/n)"
if ($dockerInstall -eq 'y' -or $dockerInstall -eq 'Y') {
    Write-Host "添加 Docker GPG 密钥..." -ForegroundColor Gray
    wsl -d $DistributionName -- bash -c "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg"
    
    Write-Host "添加 Docker 仓库..." -ForegroundColor Gray
    wsl -d $DistributionName -- bash -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'
    
    Write-Host "更新软件包列表..." -ForegroundColor Gray
    wsl -d $DistributionName -- sudo apt update
    
    Write-Host "安装 Docker..." -ForegroundColor Gray
    wsl -d $DistributionName -- sudo apt install -y docker-ce docker-ce-cli containerd.io
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker 安装完成" -ForegroundColor Green
        
        # 添加到 docker 组（避免每次都用 sudo）
        wsl -d $DistributionName -- sudo usermod -aG docker $env:USERNAME
        Write-Host "提示：重启 WSL 后可以直接使用 docker 命令" -ForegroundColor Yellow
    } else {
        Write-Host "⚠ Docker 安装失败" -ForegroundColor Yellow
    }
} else {
    Write-Host "跳过 Docker 安装" -ForegroundColor Cyan
}

Write-Host "`n[6/6] 配置 Git..." -ForegroundColor Green
Write-Host "设置 Git 用户名和邮箱..." -ForegroundColor Gray
$gitName = Read-Host "请输入 Git 用户名 (留空使用默认值)"
$gitEmail = Read-Host "请输入 Git 邮箱 (留空使用默认值)"

if ([string]::IsNullOrWhiteSpace($gitName)) {
    $gitName = "Developer"
}
if ([string]::IsNullOrWhiteSpace($gitEmail)) {
    $gitEmail = "developer@example.com"
}

wsl -d $DistributionName -- git config --global user.name "$gitName"
wsl -d $DistributionName -- git config --global user.email "$gitEmail"
wsl -d $DistributionName -- git config --global core.autocrlf input

Write-Host "✓ Git 配置完成" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   开发环境配置完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "已安装的工具:" -ForegroundColor Yellow
Write-Host "  ✓ Git" -ForegroundColor Green
Write-Host "  ✓ Python3 + pip" -ForegroundColor Green
Write-Host "  ✓ Node.js + npm" -ForegroundColor Green
if ($dockerInstall -eq 'y' -or $dockerInstall -eq 'Y') {
    Write-Host "  ✓ Docker" -ForegroundColor Green
}
Write-Host "  ✓ 基础开发工具" -ForegroundColor Green

Write-Host "`n验证命令:" -ForegroundColor Yellow
Write-Host "  wsl -d $DistributionName -- git --version" -ForegroundColor White
Write-Host "  wsl -d $DistributionName -- python3 --version" -ForegroundColor White
Write-Host "  wsl -d $DistributionName -- node --version" -ForegroundColor White
Write-Host "  wsl -d $DistributionName -- npm --version" -ForegroundColor White
if ($dockerInstall -eq 'y' -or $dockerInstall -eq 'Y') {
    Write-Host "  wsl -d $DistributionName -- docker --version" -ForegroundColor White
}

Write-Host "`n提示:" -ForegroundColor Yellow
Write-Host "  1. 首次启动 WSL 需要设置用户密码" -ForegroundColor White
Write-Host "  2. Windows 文件位于 /mnt/c/, /mnt/d/ 等路径" -ForegroundColor White
Write-Host "  3. 可以使用 VSCode Remote - WSL 扩展进行开发" -ForegroundColor White
Write-Host ""
