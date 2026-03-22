#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confighub.settings')
django.setup()

from django.db import connection
from smart_permission.models import SmartPermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

print("=== 检查数据库表 ===")
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"数据库中的表: {tables}")

print("\n=== 检查 SmartPermission 表数据 ===")
smart_perms = SmartPermission.objects.all()
print(f"SmartPermission 记录数: {smart_perms.count()}")
for p in smart_perms:
    print(f"  - {p.name} (codename: {p.codename}, type: {p.permission_type})")

print("\n=== 检查 ContentType ===")
content_type = ContentType.objects.get_for_model(SmartPermission)
print(f"SmartPermission 的 ContentType: {content_type}")
print(f"  - id: {content_type.id}")
print(f"  - app_label: {content_type.app_label}")
print(f"  - model: {content_type.model}")

print("\n=== 检查 auth_permission 表数据 ===")
auth_perms = Permission.objects.filter(content_type=content_type)
print(f"关联的 Permission 记录数: {auth_perms.count()}")
for p in auth_perms:
    print(f"  - {p.name} (codename: {p.codename})")
    print(f"    是否以'Can '开头: {p.name.startswith('Can ')}")

print("\n=== 检查 get_all_defined_permissions 结果 ===")
from smart_permission.views import get_all_defined_permissions, get_smart_permission_content_type
ct = get_smart_permission_content_type()
print(f"get_smart_permission_content_type() 返回: {ct}")
all_perms = get_all_defined_permissions()
print(f"get_all_defined_permissions() 返回: {all_perms}")
