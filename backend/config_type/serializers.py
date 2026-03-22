from rest_framework import serializers
from .models import ConfigType


class ConfigTypeSerializer(serializers.ModelSerializer):
    """配置类型序列化器"""
    instance_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ConfigType
        fields = ['id', 'name', 'title', 'description', 'format', 'schema', 
                  'instance_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_instance_count(self, obj):
        return obj.configinstance_set.count()
    
    def validate_name(self, value):
        """验证名称格式"""
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError("名称只能包含字母、数字和下划线")
        return value
    
    def validate_schema(self, value):
        """验证 JSON Schema 格式"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Schema 必须是 JSON 对象")
        if value and 'type' not in value:
            raise serializers.ValidationError("Schema 必须包含 type 字段")
        return value
