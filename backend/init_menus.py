#!/usr/bin/env python
"""
初始化菜单数据脚本
将原有的硬编码菜单导入到数据库中
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confighub.settings')
django.setup()

from smart_permission.models import Menu, SmartPermission


def init_menus():
    """初始化菜单数据"""
    
    # 定义菜单数据（与原来前端硬编码的菜单对应）
    menus_data = [
        {
            'name': '首页',
            'title': '首页',
            'path': '/',
            'icon': 'HomeFilled',
            'component': 'Home',
            'sort_order': 1,
        },
        {
            'name': '配置类型',
            'title': '配置类型',
            'path': '/types',
            'icon': 'Document',
            'component': 'ConfigTypeList',
            'sort_order': 2,
        },
        {
            'name': '配置实例',
            'title': '配置实例',
            'path': '/instances',
            'icon': 'Files',
            'component': 'ConfigInstanceList',
            'sort_order': 3,
        }
    ]
    
    print("开始初始化菜单数据...")
    
    for menu_data in menus_data:
        # 尝试查找关联的权限
        permission = None
        try:
            # 查找以菜单名开头的权限
            permission = SmartPermission.objects.filter(
                name__startswith=menu_data['name']
            ).first()
        except Exception as e:
            print(f"  查找权限失败 {menu_data['name']}: {e}")
        
        # 创建或更新菜单
        menu, created = Menu.objects.update_or_create(
            name=menu_data['name'],
            defaults={
                'title': menu_data['title'],
                'path': menu_data['path'],
                'icon': menu_data['icon'],
                'component': menu_data['component'],
                'sort_order': menu_data['sort_order'],
                'is_active': True,
                'permission': permission
            }
        )
        
        action = "创建" if created else "更新"
        print(f"  {action}菜单: {menu.name} ({menu.title})")
        if permission:
            print(f"    关联权限: {permission.name}")
    
    print(f"\n菜单初始化完成！共处理 {len(menus_data)} 个菜单")


if __name__ == '__main__':
    init_menus()
