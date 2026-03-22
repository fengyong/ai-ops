from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


def get_smart_permission_content_type():
    try:
        return ContentType.objects.get_for_model(SmartPermission)
    except:
        return None


class SmartPermission(models.Model):
    name = models.CharField(_("name"), max_length=255, help_text="权限名称，如：配置实例.新建配置实例")
    codename = models.CharField(_("codename"), max_length=100, default="")
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_("content type"),
        default=get_smart_permission_content_type,
    )
    description = models.TextField(max_length=256, blank=True, null=True, default="", verbose_name="权限描述")
    permission_type = models.CharField(
        max_length=20,
        choices=[('menu', '菜单权限'), ('button', '按钮权限')],
        default='button',
        verbose_name='权限类型'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def permission_code(self):
        return self.content_type.app_label + "." + self.codename

    class Meta:
        verbose_name = _("smart_permission")
        verbose_name_plural = _("smart_permissions")
        unique_together = [["content_type", "codename"]]
        ordering = ["name"]
        db_table = "smart_permission"

    def __str__(self):
        return f"{self.name} ({self.permission_type})"

    def save(self, *args, **kwargs):
        # 先保存 SmartPermission
        super().save(*args, **kwargs)
        # 同步创建/更新 Django Permission 记录
        self._sync_permission()

    def _sync_permission(self):
        """同步创建或更新 Django Permission 记录"""
        content_type = self.content_type or get_smart_permission_content_type()
        if not content_type:
            return

        Permission.objects.get_or_create(
            codename=self.codename,
            content_type=content_type,
            defaults={'name': self.name}
        )

    def delete(self, *args, **kwargs):
        # 删除对应的 Django Permission 记录
        content_type = self.content_type or get_smart_permission_content_type()
        if content_type:
            Permission.objects.filter(
                codename=self.codename,
                content_type=content_type
            ).delete()
        super().delete(*args, **kwargs)


class UserRole(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='角色名称')
    description = models.TextField(max_length=256, blank=True, null=True, default="", verbose_name='角色描述')
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name='权限列表')
    users = models.ManyToManyField(User, blank=True, verbose_name='用户列表')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_role"
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色'

    def __str__(self):
        return self.name


class Menu(models.Model):
    """动态菜单配置 - 支持后端驱动的前端菜单"""
    name = models.CharField(max_length=100, unique=True, verbose_name='菜单标识')
    title = models.CharField(max_length=100, verbose_name='菜单标题')
    path = models.CharField(max_length=200, verbose_name='路由路径')
    icon = models.CharField(max_length=50, blank=True, default='', verbose_name='图标名称')
    component = models.CharField(max_length=100, blank=True, default='', verbose_name='组件名称',
                                  help_text='Vue组件名称，如 ConfigTypeList, ConfigInstanceList')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='父菜单', related_name='children')
    permission = models.ForeignKey(SmartPermission, null=True, blank=True,
                                   on_delete=models.SET_NULL, verbose_name='关联权限')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "smart_menu"
        verbose_name = '菜单配置'
        verbose_name_plural = '菜单配置'
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return self.title
