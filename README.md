# ConfigHub - 配置管理中心

一个基于 Django + Vue3 的配置文件管理系统，支持 JSON/TOML 格式，具备可视化表单编辑、版本管理和审计功能。

## 系统访问

### 前端界面
- **地址**: http://localhost:3000/
- **功能**: 配置类型管理、配置实例管理（支持表单/代码双模式编辑）

### 管理后台 (Django Admin)
- **地址**: http://localhost:8000/admin/
- **账号**: `admin`
- **密码**: `admin123`

### API 接口
- **根路径**: http://localhost:8000/
- **配置类型**: http://localhost:8000/api/types/
- **配置实例**: http://localhost:8000/api/instances/

## 核心功能

### 1. 配置类型管理
- 定义配置模板，支持 JSON Schema 约束
- 支持 JSON/TOML 两种格式
- Schema 可视化编辑（表单 + 代码双模式）

### 2. 配置实例管理
- **JSON 格式**: 支持表单编辑（基于 JSON Schema）和代码编辑（Monaco 编辑器）
- **TOML 格式**: 支持代码编辑（Monaco 编辑器）
- 自动格式验证和 Schema 校验
- 实时预览和错误提示

### 3. 版本控制
- 自动版本管理（每次保存递增版本号）
- 支持历史版本查看和回滚
- 版本对比功能

### 4. 审计日志
- 记录所有创建、更新、删除操作
- 包含操作人、时间、变更内容

## 快速开始

### 环境要求

- Python 3.13+
- Node.js 20+
- (可选) Docker & Docker Compose

### 方式一：本地开发启动

#### 1. 启动后端服务

```bash
cd backend

# 创建虚拟环境（首次）
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安装依赖（首次）
pip install -r requirements.txt

# 运行数据库迁移（首次）
python manage.py migrate

# 启动服务
python manage.py runserver 0.0.0.0:8000
```

后端服务将在 http://localhost:8000/ 启动

#### 2. 启动前端服务

```bash
cd frontend

# 安装依赖（首次）
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:3000/ 启动

#### 3. 初始化菜单数据（首次）

```bash
cd backend
python init_menus.py
```

### 方式二：Docker 启动

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 访问系统

- **前端界面**: http://localhost:3000/
- **管理后台**: http://localhost:8000/admin/

## 使用指南

### 创建配置类型

1. 进入前端界面，点击"配置类型" → "新建类型"
2. 填写类型标识（如 `app_theme`）、显示名称
3. 选择格式（JSON 或 TOML）
4. 定义 JSON Schema（支持表单编辑或代码编辑）
5. 保存

### 创建配置实例

1. 点击"配置实例" → "新建实例"
2. 选择配置类型
3. 填写实例名称
4. 根据格式选择编辑方式：
   - **JSON + 有 Schema**: 可选择"表单编辑"或"代码编辑"
   - **TOML 或无 Schema**: 使用"代码编辑"
5. 填写配置内容并保存

### API 使用示例

```bash
# 获取配置类型列表
curl http://localhost:8000/api/types/

# 获取配置实例列表
curl http://localhost:8000/api/instances/

# 创建配置类型
curl -X POST http://localhost:8000/api/types/ \
  -H "Content-Type: application/json" \
  -d '{"name":"db_config","title":"Database Config","format":"json","schema":{}}'

# 创建配置实例
curl -X POST http://localhost:8000/api/instances/ \
  -H "Content-Type: application/json" \
  -d '{"config_type":1,"name":"production_db","format":"json","content":"{\"host\":\"localhost\"}"}'
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 6.0 + Django REST Framework |
| 前端 | Vue 3 + Vite + Element Plus |
| 编辑器 | @json-editor/json-editor + CodeMirror |
| 数据库 | SQLite (开发) / MySQL 8.0 (生产) |
| 部署 | Docker + Docker Compose |

## 项目结构

```
ai-ops/
├── backend/                 # Django 后端
│   ├── config_type/         # 配置类型应用
│   ├── config_instance/     # 配置实例应用
│   ├── versioning/          # 版本管理应用
│   ├── audit/               # 审计日志应用
│   └── manage.py
├── frontend/                # Vue 前端
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   ├── components/      # 通用组件
│   │   │   ├── JsonSchemaEditor.vue   # JSON Schema 表单编辑器
│   │   │   └── CodeEditor.vue         # 代码编辑器
│   │   └── api/             # API 接口
│   └── package.json
├── design/                  # 设计文档
│   ├── review/              # 代码审查报告
│   └── issue/               # 问题记录
└── docker-compose.yml
```

## 默认数据

系统已预置测试数据：
- **配置类型**: Database Configuration, Application Settings, Server Configuration (TOML), App Theme
- **配置实例**: production_db, production_server (TOML, 59行)

## 注意事项

1. 当前为开发模式 (DEBUG=True)
2. CORS 允许所有来源 (开发便利)
3. 生产部署前请修改安全配置
4. 前端使用 Element Plus 默认主题

## 更多信息

查看 `design/review/` 目录获取详细的代码审查报告。
