from django.contrib import admin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType
from .models import SmartPermission, UserRole, Menu


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'content_type', 'get_app_label']
    list_filter = ['content_type__app_label', 'content_type']
    search_fields = ['name', 'codename']
    ordering = ['content_type__app_label', 'codename']
    
    def get_app_label(self, obj):
        return obj.content_type.app_label if obj.content_type else '-'
    get_app_label.short_description = '应用'
    get_app_label.admin_order_field = 'content_type__app_label'


@admin.register(SmartPermission)
class SmartPermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'permission_type', 'description', 'created_at', 'updated_at']
    list_filter = ['permission_type', 'created_at']
    search_fields = ['name', 'codename', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'codename', 'permission_type', 'description')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_users_count', 'get_permissions_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['permissions', 'users']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description')
        }),
        ('权限配置', {
            'fields': ('permissions',)
        }),
        ('用户配置', {
            'fields': ('users',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_users_count(self, obj):
        return obj.users.count()
    get_users_count.short_description = '用户数量'
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()
    get_permissions_count.short_description = '权限数量'


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'path', 'icon', 'component', 'permission', 'sort_order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'title', 'path']
    list_editable = ['sort_order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'title', 'path', 'icon', 'component')
        }),
        ('权限配置', {
            'fields': ('permission',),
            'description': '关联权限后，只有拥有该权限的用户才能看到此菜单'
        }),
        ('层级结构', {
            'fields': ('parent',),
            'description': '设置父菜单可创建多级菜单'
        }),
        ('显示控制', {
            'fields': ('sort_order', 'is_active')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class UserRoleInline(admin.TabularInline):
    model = UserRole.users.through
    extra = 0
    verbose_name = '用户角色'
    verbose_name_plural = '用户角色'


class CustomUserAdmin(UserAdmin):
    inlines = [UserRoleInline]
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
