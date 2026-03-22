#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confighub.settings')
django.setup()

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from smart_permission.models import SmartPermission, get_smart_permission_content_type

print("=== 修复权限数据 ===")

# 获取 ContentType
content_type = get_smart_permission_content_type()
print(f"ContentType: {content_type}")

# 遍历所有 SmartPermission，创建对应的 Permission
smart_perms = SmartPermission.objects.all()
print(f"\n发现 {smart_perms.count()} 个 SmartPermission 记录")

for sp in smart_perms:
    print(f"\n处理: {sp.name} (codename: {sp.codename})")
    
    # 检查是否已存在对应的 Permission
    existing = Permission.objects.filter(
        codename=sp.codename,
        content_type=content_type
    ).first()
    
    if existing:
        print(f"  -> 已存在 Permission: {existing.name}")
        # 更新 name 保持一致
        if existing.name != sp.name:
            existing.name = sp.name
            existing.save()
            print(f"  -> 已更新 name 为: {sp.name}")
    else:
        # 创建新的 Permission
        perm = Permission.objects.create(
            name=sp.name,
            codename=sp.codename,
            content_type=content_type
        )
        print(f"  -> 已创建 Permission: {perm.name}")

print("\n=== 验证修复结果 ===")
auth_perms = Permission.objects.filter(content_type=content_type)
print(f"关联的 Permission 记录数: {auth_perms.count()}")
for p in auth_perms:
    print(f"  - {p.name} (codename: {p.codename})")
    print(f"    是否以'Can '开头: {p.name.startswith('Can ')}")

# 测试 get_all_defined_permissions
from smart_permission.views import get_all_defined_permissions
all_perms = get_all_defined_permissions()
print(f"\nget_all_defined_permissions() 返回: {all_perms}")
