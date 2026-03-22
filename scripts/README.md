# WSL 安装与配置指南

本目录包含三个 PowerShell 脚本，用于完整安装和配置 WSL (Windows Subsystem for Linux) 开发环境。

## 📋 前提条件

### 方式 1: 从微软应用商店安装（推荐）

1. **打开 Microsoft Store**
   - 按 `Win + S`，搜索 "Microsoft Store"

2. **搜索 Ubuntu 22.04**
   - 在商店中搜索 "Ubuntu 22.04"
   - 找到 "Ubuntu 22.04 LTS" by Canonical Group Limited

3. **点击获取/安装**
   - 点击 "获取" 或 "安装" 按钮
   - 等待下载和安装完成

4. **运行脚本**
   - 脚本会自动查找已安装的 Ubuntu 镜像
   - 直接运行即可，无需手动指定路径

### 方式 2: 从 GitHub 下载官方镜像

1. **访问 WSL GitHub releases**
   - 网址：https://github.com/microsoft/WSL/releases

2. **下载 Ubuntu 22.04 镜像**
   - 找到最新的 release
   - 下载 `Ubuntu-22.04.appx` 或 `.msixbundle` 文件

3. **记录下载路径**
   - 通常在 `C:\Users\你的用户名\Downloads\`

### 方式 3: 使用 wsl --install 在线安装（最简单）

如果不想手动下载，可以直接使用：

```powershell
# 以管理员身份运行 PowerShell
wsl --install -d Ubuntu-22.04
```

这会自动下载并安装 Ubuntu 22.04（需要网络连接）。

---

## ⚙️ 高级选项

### 自定义安装路径

```powershell
# 指定镜像文件路径
.\install-wsl.ps1 -DownloadFilePath "D:\Downloads\Ubuntu-22.04.appx"

# 指定 WSL 安装位置
.\install-wsl.ps1 -WSLInstallPath "E:\WSL\Ubuntu2204"

# 同时指定两个参数
.\install-wsl.ps1 `
    -DownloadFilePath "D:\Downloads\Ubuntu-22.04.appx" `
    -WSLInstallPath "E:\WSL\Ubuntu2204"
```

2. **管理员权限**
   - 所有脚本需要以管理员身份运行
   - 右键点击脚本 → "以管理员身份运行"

## 🔧 脚本说明

### 1. install-wsl.ps1 - WSL 离线安装脚本

**功能：**
- 启用 WSL 功能
- 自动查找或导入 Ubuntu 发行版
- 配置 WSL 2 版本
- 设置为默认发行版
- 支持自动检测已安装的 Ubuntu 镜像

**使用方法：**
```powershell
# 方式 1: 自动查找镜像（推荐）
# 如果在微软商店安装了 Ubuntu，脚本会自动找到
.\install-wsl.ps1

# 方式 2: 指定镜像文件路径
.\install-wsl.ps1 -DownloadFilePath "D:\Downloads\Ubuntu-22.04.appx"

# 方式 3: 自定义所有参数
.\install-wsl.ps1 `
    -DownloadFilePath "C:\path\to\Ubuntu-22.04.appx" `
    -WSLInstallPath "D:\WSL\Ubuntu2204" `
    -DistributionName "Ubuntu-22.04"
```

**参数说明：**
- `-DownloadFilePath`: Ubuntu 镜像文件路径（可选，留空则自动查找）
- `-WSLInstallPath`: WSL 安装目录（默认：D:\WSL\Ubuntu2204）
- `-DistributionName`: 发行版名称（默认：Ubuntu-22.04）

---

### 2. verify-wsl.ps1 - WSL 验证脚本

**功能：**
- 检查 WSL 安装状态
- 验证发行版是否正确导入
- 测试 WSL 启动和基本命令
- 检查网络连接和文件系统

**使用方法：**
```powershell
# 验证默认发行版
.\verify-wsl.ps1

# 验证指定发行版
.\verify-wsl.ps1 -DistributionName "Ubuntu2204"
```

---

### 3. setup-wsl-dev.ps1 - WSL 开发环境配置脚本

**功能：**
- 安装 Git、curl、wget、vim 等基础工具
- 安装 Python3 + pip + venv
- 安装 Node.js + npm
- 可选安装 Docker
- 配置 Git 用户信息

**使用方法：**
```powershell
# 使用默认配置
.\setup-wsl-dev.ps1

# 指定发行版
.\setup-wsl-dev.ps1 -DistributionName "Ubuntu2204"
```

**安装的工具：**
- ✅ Git
- ✅ Python3 + pip + venv
- ✅ Node.js 18.x + npm
- ✅ Docker（可选）
- ✅ 基础开发工具（curl, wget, vim, net-tools 等）

---

## 🚀 完整安装流程

### 步骤 1: 获取 Ubuntu 22.04（选择一种方式）

**推荐方式 - 微软应用商店:**
```
1. 打开 Microsoft Store
2. 搜索 "Ubuntu 22.04"
3. 点击 "获取" 安装
```

**或者 - GitHub 下载:**
```
1. 访问：https://github.com/microsoft/WSL/releases
2. 下载：Ubuntu-22.04.appx
```

**或者直接在线安装:**
```powershell
wsl --install -d Ubuntu-22.04
```

### 步骤 2: 安装 WSL
```powershell
# 以管理员身份运行
.\install-wsl.ps1
```

**注意：** 如果提示需要重启，请重启电脑后重新运行脚本。

### 步骤 3: 首次启动 WSL
```powershell
wsl
```
- 设置用户名（小写字母，无空格）
- 设置密码（输入时不显示）
- 确认密码

### 步骤 4: 验证安装
```powershell
.\verify-wsl.ps1
```

### 步骤 5: 配置开发环境
```powershell
# 以管理员身份运行
.\setup-wsl-dev.ps1
```

按照提示选择是否安装 Docker，并配置 Git 用户信息。

---

## 📝 常用 WSL 命令

```powershell
# 启动 WSL
wsl

# 启动指定发行版
wsl -d Ubuntu2204

# 查看已安装的发行版
wsl --list --verbose

# 关闭 WSL
wsl --shutdown

# 导出 WSL 发行版（备份）
wsl --export Ubuntu2204 D:\backup\ubuntu-backup.tar

# 导入 WSL 发行版（恢复）
wsl --import Ubuntu2204 D:\WSL\Ubuntu2204 D:\backup\ubuntu-backup.tar

# 注销发行版（删除）
wsl --unregister Ubuntu2204
```

---

## 🔍 故障排查

### 问题 1: 脚本无法执行
**解决方案：** 允许执行 PowerShell 脚本
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题 2: WSL 功能无法启用
**解决方案：** 手动启用 Windows 功能
1. 控制面板 → 程序和功能 → 启用或关闭 Windows 功能
2. 勾选：
   - ✅ 适用于 Linux 的 Windows 子系统
   - ✅ 虚拟机平台
3. 重启电脑

### 问题 3: 导入失败
**可能原因：** 
- 下载文件损坏
- 路径包含中文或特殊字符
- 磁盘空间不足

**解决方案：**
- 重新下载 Ubuntu 镜像
- 使用英文路径
- 检查磁盘空间

### 问题 4: WSL 2 转换失败
**解决方案：**
```powershell
# 检查虚拟化是否启用
任务管理器 → 性能 → CPU → 虚拟化：已启用

# 如未启用，需在 BIOS 中开启 VT-x/AMD-V
```

---

## 💡 使用技巧

### 1. Windows 与 WSL 文件互访
```bash
# WSL 访问 Windows 文件
cd /mnt/c/Users/你的用户名

# Windows 访问 WSL 文件
\\wsl$\Ubuntu2204\home\你的用户名
```

### 2. VSCode Remote - WSL
1. 安装 VSCode
2. 安装扩展：Remote - WSL
3. 在 WSL 终端中输入：`code .`

### 3. 修改 WSL 安装位置
```powershell
# 导出当前安装
wsl --export Ubuntu2204 D:\ubuntu-backup.tar

# 注销原安装
wsl --unregister Ubuntu2204

# 导入到新位置
wsl --import Ubuntu2204 D:\NewPath\D:\ubuntu-backup.tar
```

---

## 📞 获取帮助

如遇问题，可以：
1. 查看脚本输出日志
2. 运行验证脚本诊断问题
3. 参考 Microsoft 官方文档：https://docs.microsoft.com/windows/wsl/

---

## ⚠️ 注意事项

1. **管理员权限**: 所有脚本需要管理员权限
2. **重启要求**: 首次启用 WSL 功能后需要重启
3. **虚拟化支持**: 需要在 BIOS 中启用 CPU 虚拟化
4. **磁盘空间**: 建议至少预留 10GB 空间
5. **网络要求**: 安装开发工具时需要网络连接

---

**祝您使用愉快！** 🎉
