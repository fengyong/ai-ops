from django.db import models


class ConfigType(models.Model):
    """配置类型定义"""
    FORMAT_CHOICES = [
        ('json', 'JSON'),
        ('toml', 'TOML'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name='类型标识')
    title = models.CharField(max_length=200, verbose_name='显示名称')
    description = models.TextField(blank=True, verbose_name='描述')
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='json', verbose_name='格式')
    schema = models.JSONField(default=dict, verbose_name='JSON Schema')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'config_type'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.name})"
