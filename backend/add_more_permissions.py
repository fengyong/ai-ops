#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confighub.settings')
django.setup()

from smart_permission.models import SmartPermission

print("=== 添加更多权限按钮 ===")

# 定义要添加的权限
permissions_to_add = [
    # 配置实例相关权限
    {'name': '配置实例.搜索', 'codename': 'config_instance_search', 'permission_type': 'button', 'description': '搜索配置实例'},
    {'name': '配置实例.新建', 'codename': 'config_instance_add', 'permission_type': 'button', 'description': '新建配置实例'},
    {'name': '配置实例.编辑', 'codename': 'config_instance_edit', 'permission_type': 'button', 'description': '编辑配置实例'},
    {'name': '配置实例.删除', 'codename': 'config_instance_delete', 'permission_type': 'button', 'description': '删除配置实例'},
    {'name': '配置实例.查看', 'codename': 'config_instance_view', 'permission_type': 'button', 'description': '查看配置实例详情'},
    {'name': '配置实例.回滚', 'codename': 'config_instance_rollback', 'permission_type': 'button', 'description': '回滚配置实例版本'},

    # 配置类型相关权限
    {'name': '配置类型.搜索', 'codename': 'config_type_search', 'permission_type': 'button', 'description': '搜索配置类型'},
    {'name': '配置类型.新建', 'codename': 'config_type_add', 'permission_type': 'button', 'description': '新建配置类型'},
    {'name': '配置类型.编辑', 'codename': 'config_type_edit', 'permission_type': 'button', 'description': '编辑配置类型'},
    {'name': '配置类型.删除', 'codename': 'config_type_delete', 'permission_type': 'button', 'description': '删除配置类型'},

    # 用户管理相关权限
    {'name': '用户管理.搜索', 'codename': 'user_search', 'permission_type': 'button', 'description': '搜索用户'},
    {'name': '用户管理.新建', 'codename': 'user_add', 'permission_type': 'button', 'description': '新建用户'},
    {'name': '用户管理.编辑', 'codename': 'user_edit', 'permission_type': 'button', 'description': '编辑用户'},
    {'name': '用户管理.删除', 'codename': 'user_delete', 'permission_type': 'button', 'description': '删除用户'},

    # 角色管理相关权限
    {'name': '角色管理.搜索', 'codename': 'role_search', 'permission_type': 'button', 'description': '搜索角色'},
    {'name': '角色管理.新建', 'codename': 'role_add', 'permission_type': 'button', 'description': '新建角色'},
    {'name': '角色管理.编辑', 'codename': 'role_edit', 'permission_type': 'button', 'description': '编辑角色'},
    {'name': '角色管理.删除', 'codename': 'role_delete', 'permission_type': 'button', 'description': '删除角色'},
    {'name': '角色管理.分配权限', 'codename': 'role_assign_perm', 'permission_type': 'button', 'description': '为角色分配权限'},
]

added_count = 0
skipped_count = 0

for perm_data in permissions_to_add:
    # 检查是否已存在
    existing = SmartPermission.objects.filter(codename=perm_data['codename']).first()
    if existing:
        print(f"跳过（已存在）: {perm_data['name']}")
        skipped_count += 1
    else:
        SmartPermission.objects.create(**perm_data)
        print(f"创建成功: {perm_data['name']}")
        added_count += 1

print(f"\n=== 完成 ===")
print(f"新增权限: {added_count} 个")
print(f"跳过（已存在）: {skipped_count} 个")

# 显示所有权限
print(f"\n=== 当前所有权限 ===")
all_perms = SmartPermission.objects.all().order_by('name')
for p in all_perms:
    print(f"  - {p.name} ({p.permission_type})")
