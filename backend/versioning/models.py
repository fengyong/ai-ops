from django.db import models
from django.contrib.auth.models import User


class ConfigVersion(models.Model):
    """配置版本历史"""
    config = models.ForeignKey('config_instance.ConfigInstance', on_delete=models.CASCADE, related_name='versions')
    version = models.PositiveIntegerField(verbose_name='版本号')
    format = models.CharField(max_length=10, verbose_name='格式')
    content_text = models.TextField(verbose_name='原始内容')
    parsed_data = models.JSONField(default=dict, verbose_name='解析后数据')
    change_reason = models.TextField(blank=True, verbose_name='变更说明')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='修改者')
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'config_version'
        unique_together = ['config', 'version']
        ordering = ['-version']
    
    def __str__(self):
        return f"{self.config.name} v{self.version}"
