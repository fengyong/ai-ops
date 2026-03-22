from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    """审计日志"""
    ACTION_CHOICES = [
        ('CREATE', '创建'),
        ('UPDATE', '更新'),
        ('DELETE', '删除'),
        ('VIEW', '查看'),
        ('EXPORT', '导出'),
        ('IMPORT', '导入'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='操作类型')
    resource_type = models.CharField(max_length=50, verbose_name='资源类型')
    resource_id = models.CharField(max_length=100, verbose_name='资源ID')
    resource_name = models.CharField(max_length=200, verbose_name='资源名称')
    details = models.JSONField(default=dict, verbose_name='详细信息')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_log'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} {self.action} {self.resource_type}/{self.resource_name}"
