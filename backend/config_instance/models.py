from django.db import models
from django.contrib.auth.models import User
import toml
import json


class ConfigInstance(models.Model):
    """配置实例"""
    FORMAT_CHOICES = [
        ('json', 'JSON'),
        ('toml', 'TOML'),
    ]
    
    config_type = models.ForeignKey('config_type.ConfigType', on_delete=models.CASCADE, verbose_name='配置类型')
    name = models.CharField(max_length=100, verbose_name='配置名称')
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='json', verbose_name='格式')
    
    # 原始内容存储
    content_text = models.TextField(verbose_name='原始内容')
    
    # 解析后的统一数据（用于查询、关联）
    parsed_data = models.JSONField(default=dict, verbose_name='解析后数据')
    
    version = models.PositiveIntegerField(default=1, verbose_name='版本号')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'config_instance'
        unique_together = ['config_type', 'name']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.config_type.title}/{self.name}"
    
    def save(self, *args, **kwargs):
        # 解析并验证内容
        self._parse_content()
        super().save(*args, **kwargs)
    
    def _parse_content(self):
        """解析内容为统一格式"""
        if self.format == 'json':
            try:
                self.parsed_data = json.loads(self.content_text)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON: {e}")
        elif self.format == 'toml':
            try:
                self.parsed_data = toml.loads(self.content_text)
            except toml.TomlDecodeError as e:
                raise ValueError(f"Invalid TOML: {e}")
    
    def get_as_json(self):
        """获取 JSON 格式内容"""
        return json.dumps(self.parsed_data, indent=2, ensure_ascii=False)
    
    def get_as_toml(self):
        """获取 TOML 格式内容"""
        return toml.dumps(self.parsed_data)
    
    def get_content_by_format(self, target_format=None):
        """根据格式获取内容"""
        target = target_format or self.format
        if target == 'json':
            return self.get_as_json()
        return self.get_as_toml()
