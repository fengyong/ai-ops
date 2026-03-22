from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import SmartPermission, UserRole, Menu


def get_smart_permission_content_type():
    try:
        return ContentType.objects.get_for_model(SmartPermission)
    except:
        return None


def get_side_menus(permissions):
    """
    根据权限名称推断菜单
    权限格式：菜单.按钮
    例如：配置实例.新建 -> 菜单是"配置实例"
    """
    menus = set()
    for p in permissions:
        parts = p.split('.')
        if len(parts) >= 1:
            # 只取第一级作为菜单名称
            menu = parts[0]
            menus.add(menu)
    return sorted(list(menus))


def get_all_defined_permissions():
    """
    返回SmartPermission模型中定义的所有权限名称
    """
    return list(SmartPermission.objects.values_list('name', flat=True))


def get_user_permissions(user):
    if not user.is_authenticated:
        return []

    if user.is_superuser:
        return get_all_defined_permissions()

    # 获取用户通过角色关联的所有SmartPermission
    content_type = get_smart_permission_content_type()
    if not content_type:
        return []

    # 获取用户所有角色的权限
    user_roles = UserRole.objects.filter(users=user)
    django_permissions = Permission.objects.filter(
        content_type=content_type,
        userrole__in=user_roles
    ).distinct()

    # 根据Django Permission找到对应的SmartPermission名称
    smart_perm_names = []
    for perm in django_permissions:
        try:
            smart_perm = SmartPermission.objects.get(
                codename=perm.codename,
                content_type=content_type
            )
            smart_perm_names.append(smart_perm.name)
        except SmartPermission.DoesNotExist:
            pass

    return smart_perm_names


def get_user_menus(user):
    """
    获取用户可访问的菜单列表
    超级用户返回所有启用的菜单，普通用户根据权限过滤
    """
    if not user.is_authenticated:
        return []

    # 获取所有启用的顶级菜单
    menus = Menu.objects.filter(is_active=True, parent=None)

    if user.is_superuser:
        return menus

    # 获取用户拥有的权限名称
    user_permissions = get_user_permissions(user)

    # 过滤有权限的菜单
    accessible_menus = []
    for menu in menus:
        # 菜单没有关联权限，或者用户有该权限
        if not menu.permission:
            accessible_menus.append(menu)
        elif menu.permission.name in user_permissions:
            accessible_menus.append(menu)

    return accessible_menus


def menu_to_dict(menu):
    """将菜单模型转换为字典"""
    return {
        'id': menu.id,
        'name': menu.name,
        'title': menu.title,
        'path': menu.path,
        'icon': menu.icon,
        'component': menu.component,
        'sort_order': menu.sort_order,
        'permission_name': menu.permission.name if menu.permission else None
    }


@api_view(['GET'])
@permission_classes([AllowAny])
def get_permissions(request):
    user = request.user

    user_permissions = get_user_permissions(user)
    all_permissions = get_all_defined_permissions()

    missing_permissions = list(set(all_permissions) - set(user_permissions))

    # 获取动态菜单
    user_menus = get_user_menus(user)
    menus_data = [menu_to_dict(menu) for menu in user_menus]

    # 保留side_menus用于兼容旧版本
    side_menus = [menu['name'] for menu in menus_data]

    return Response({
        'username': user.username if user.is_authenticated else None,
        'is_authenticated': user.is_authenticated,
        'is_superuser': user.is_superuser if user.is_authenticated else False,
        'side_menus': side_menus,
        'menus': menus_data,  # 新的完整菜单数据
        'missing_permissions': missing_permissions,
        'all_permissions': all_permissions
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_menus(request):
    """
    获取当前用户的菜单列表
    """
    user = request.user
    user_menus = get_user_menus(user)
    menus_data = [menu_to_dict(menu) for menu in user_menus]

    return Response({
        'username': user.username if user.is_authenticated else None,
        'is_authenticated': user.is_authenticated,
        'menus': menus_data
    })
