# ConfigHub - 配置管理中心

一个基于 Django + Vue3 的配置文件管理系统，支持 JSON/TOML 格式，具备版本管理和审计功能。

## 系统访问

### 管理后台 (Django Admin)
- **地址**: http://localhost:8000/admin/
- **账号**: `admin`
- **密码**: `admin123`

### API 接口
- **根路径**: http://localhost:8000/
- **配置类型**: http://localhost:8000/api/types/
- **配置实例**: http://localhost:8000/api/instances/

## 快速开始

### 1. 启动后端服务

```bash
cd backend
.\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

### 2. 管理后台使用

1. 访问 http://localhost:8000/admin/
2. 使用账号 `admin` / 密码 `admin123` 登录
3. 可以管理以下内容：
   - **Config Types** - 配置类型定义
   - **Config Instances** - 配置实例数据
   - **Audit Logs** - 操作审计日志
   - **Config Versions** - 版本历史

### 3. API 使用示例

```bash
# 获取配置类型列表
curl http://localhost:8000/api/types/

# 获取配置实例列表
curl http://localhost:8000/api/instances/

# 创建配置类型
curl -X POST http://localhost:8000/api/types/ \
  -H "Content-Type: application/json" \
  -d '{"name":"db_config","title":"Database Config","format":"json","schema":{}}'
```

## 功能模块

| 模块 | 描述 |
|------|------|
| 配置类型管理 | 定义配置模板，支持 JSON Schema |
| 配置实例管理 | 基于类型创建具体配置，支持 JSON/TOML |
| 版本控制 | 自动版本管理，支持历史回滚 |
| 审计日志 | 记录所有操作，便于追踪 |

## 技术栈

- **后端**: Django 6.0 + Django REST Framework
- **前端**: Vue 3 + Vite + Element Plus
- **数据库**: SQLite (开发) / MySQL 8.0 (生产)
- **部署**: Docker + Docker Compose

## 项目结构

```
ai-ops/
├── backend/          # Django 后端
│   ├── config_type/  # 配置类型应用
│   ├── config_instance/  # 配置实例应用
│   ├── versioning/   # 版本管理应用
│   ├── audit/        # 审计日志应用
│   └── manage.py
├── frontend/         # Vue 前端
│   ├── src/views/    # 页面组件
│   └── src/styles/   # 样式文件
├── design/           # 设计文档
│   ├── review/       # 代码审查报告
│   └── issue/        # 问题记录
└── docker-compose.yml
```

## 默认数据

系统已预置测试数据：
- 配置类型: Database Configuration, Application Settings
- 配置实例: production_db

## 注意事项

1. 当前为开发模式 (DEBUG=True)
2. CORS 允许所有来源 (开发便利)
3. 生产部署前请修改安全配置

## 更多信息

查看 `design/review/` 目录获取详细的代码审查报告。
