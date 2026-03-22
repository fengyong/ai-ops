from rest_framework import serializers
from jsonschema import validate, ValidationError as JsonSchemaError
from .models import ConfigInstance
from config_type.models import ConfigType


class ConfigInstanceSerializer(serializers.ModelSerializer):
    """配置实例序列化器"""
    config_type_name = serializers.CharField(source='config_type.name', read_only=True)
    config_type_title = serializers.CharField(source='config_type.title', read_only=True)
    content = serializers.CharField(write_only=True)
    
    class Meta:
        model = ConfigInstance
        fields = ['id', 'config_type', 'config_type_name', 'config_type_title',
                  'name', 'format', 'content', 'content_text', 'parsed_data',
                  'version', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['content_text', 'parsed_data', 'version', 'created_by', 'created_at', 'updated_at']
    
    def validate(self, data):
        """验证配置内容"""
        config_type = data.get('config_type')
        format_type = data.get('format', 'json')
        content = data.pop('content', '')
        
        # 验证内容格式
        try:
            if format_type == 'json':
                import json
                parsed = json.loads(content)
            else:  # toml
                import toml
                parsed = toml.loads(content)
        except Exception as e:
            raise serializers.ValidationError(f"内容格式错误: {e}")
        
        # 使用 JSON Schema 验证
        if config_type and config_type.schema:
            try:
                validate(instance=parsed, schema=config_type.schema)
            except JsonSchemaError as e:
                raise serializers.ValidationError(f"Schema 验证失败: {e.message}")
        
        # 将解析后的内容保存
        data['parsed_data'] = parsed
        data['content_text'] = content
        
        return data


class ConfigInstanceListSerializer(serializers.ModelSerializer):
    """配置实例列表序列化器（简化版）"""
    config_type_name = serializers.CharField(source='config_type.name', read_only=True)
    config_type_title = serializers.CharField(source='config_type.title', read_only=True)
    
    class Meta:
        model = ConfigInstance
        fields = ['id', 'config_type', 'config_type_name', 'config_type_title',
                  'name', 'format', 'version', 'created_at', 'updated_at']
