# 智能权限系统设计文档

## 设计理念

权限系统采用**简单直白**的命名和匹配规则，无需复杂的配置，完全自动化。

## 权限命名规则

权限名称 = `菜单名.按钮名`

### 示例
- `配置实例.新建` - 配置实例页面的新建按钮
- `配置实例.删除` - 配置实例页面的删除按钮
- `配置实例.重置` - 配置实例页面的重置按钮
- `配置类型.编辑` - 配置类型页面的编辑按钮

## 权限推断逻辑

### 1. 菜单权限推断
- 用户拥有 `配置实例.新建` 权限 → 可以访问"配置实例"菜单
- 用户拥有 `配置类型.查看` 权限 → 可以访问"配置类型"菜单
- **规则**: 只要有该菜单下的任意按钮权限，就可以访问该菜单

### 2. 按钮权限过滤
- 后端返回 `missing_permissions` 列表
- 前端拦截器自动匹配：`菜单名.按钮名`
- 如果权限在 `missing_permissions` 中 → 按钮隐藏
- 如果权限不在 `missing_permissions` 中 → 按钮显示

## API接口

### 获取权限接口
```
GET /api/permissions/
```

### 返回数据结构
```json
{
  "side_menus": ["配置实例", "配置类型"],
  "missing_permissions": ["配置实例.删除", "配置实例.重置"],
  "all_permissions": ["配置实例.新建", "配置实例.删除", "配置实例.编辑", "配置实例.重置", "配置实例.查看", "配置类型.新建", "配置类型.编辑", "配置类型.查看"]
}
```

### 字段说明
- `side_menus`: 用户可访问的菜单列表（从权限中自动推断）
- `missing_permissions`: 用户缺失的权限列表
- `all_permissions`: 系统中所有定义的权限列表

## 前端实现

### 权限拦截器
位置: `frontend/src/permission/interceptor.js`

核心逻辑:
1. 拦截所有组件的渲染过程
2. 识别按钮组件（ElButton）
3. 提取按钮文本内容
4. 推断权限名称: `route.meta.permission.按钮文本`
5. 检查权限是否在 `missing_permissions` 中
6. 如果缺失 → 返回 null（按钮不渲染）
7. 如果拥有 → 返回 vnode（按钮正常渲染）

### 权限Store
位置: `frontend/src/stores/permission.js`

提供方法:
- `fetchPermissions()` - 从后端获取权限数据
- `hasPermission(permissionName)` - 检查是否拥有某个权限
- `hasMenuPermission(menuName)` - 检查是否拥有某个菜单权限

## 后端实现

### 权限模型
位置: `backend/smart_permission/models.py`

- `SmartPermission` - 智能权限模型
- `UserRole` - 用户角色模型

### 权限API
位置: `backend/smart_permission/views.py`

核心函数:
- `get_side_menus(permissions)` - 从权限列表推断菜单
- `get_all_defined_permissions()` - 获取所有定义的权限
- `get_user_permissions(user)` - 获取用户拥有的权限

### 权限推断算法
```python
def get_side_menus(permissions):
    menus = set()
    for p in permissions:
        parts = p.split('.')
        if len(parts) >= 1:
            menu = parts[0]  # 只取第一级作为菜单名称
            menus.add(menu)
    return sorted(list(menus))
```

## 使用流程

1. **用户登录** → 调用 `/api/login/`
2. **登录成功** → 调用 `/api/permissions/` 获取权限
3. **权限拦截** → 在组件渲染时自动过滤按钮
4. **按钮显示** → 根据权限决定是否显示

## 权限管理

### Django Admin后台
访问: `http://127.0.0.1:8000/admin/`

可以管理:
- Smart Permissions（智能权限） - 创建、编辑、删除权限
- User Roles（用户角色） - 创建角色、分配权限、分配用户

### 创建新权限
1. 登录Django Admin
2. 进入 Smart Permissions
3. 添加新权限，格式: `菜单名.按钮名`
4. 保存后立即生效，无需修改代码

## 设计优势

1. **零配置** - 不需要在前端代码中配置权限
2. **自动化** - 权限名称自动推断，按钮自动过滤
3. **直观** - 权限名称直接对应界面元素
4. **灵活** - 可以随时添加、删除权限
5. **可扩展** - 支持任意层级的权限结构

## 注意事项

1. **按钮文案必须准确** - 权限名称中的按钮名必须与按钮文案完全一致
2. **路由配置** - 每个路由必须设置 `meta.permission` 作为菜单名
3. **权限格式** - 权限名称格式必须是 `菜单名.按钮名`
4. **登录后刷新** - 登录成功后必须重新获取权限

## 示例场景

### 场景1: 新增权限
需求: 在配置实例页面添加"导出"按钮

步骤:
1. 在Django Admin中创建权限: `配置实例.导出`
2. 在前端页面添加按钮: `<el-button>导出</el-button>`
3. 系统自动识别并应用权限控制

### 场景2: 分配权限
需求: 给testuser分配"删除"权限

步骤:
1. 登录Django Admin
2. 进入 Users → testuser
3. 在 User permissions 中添加 `配置实例.删除`
4. testuser 重新登录后即可看到删除按钮

## 技术栈

- **后端**: Django + Django REST Framework
- **前端**: Vue 3 + Element Plus + Pinia
- **认证**: Django Session Authentication
- **权限存储**: Django Permission System
