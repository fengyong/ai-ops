from rest_framework import viewsets
from rest_framework.response import Response
from .models import ConfigVersion


class ConfigVersionViewSet(viewsets.ReadOnlyModelViewSet):
    """配置版本管理 API"""
    queryset = ConfigVersion.objects.all()
    
    def list(self, request):
        """获取版本列表"""
        config_id = request.query_params.get('config_id')
        if config_id:
            queryset = ConfigVersion.objects.filter(config_id=config_id)
        else:
            queryset = ConfigVersion.objects.all()
        
        data = [{
            'id': v.id,
            'config_id': v.config_id,
            'version': v.version,
            'format': v.format,
            'change_reason': v.change_reason,
            'changed_by': v.changed_by.username if v.changed_by else None,
            'changed_at': v.changed_at,
        } for v in queryset]
        
        return Response(data)
    
    def retrieve(self, request, pk=None):
        """获取单个版本详情"""
        version = self.get_object()
        data = {
            'id': version.id,
            'config_id': version.config_id,
            'version': version.version,
            'format': version.format,
            'content_text': version.content_text,
            'parsed_data': version.parsed_data,
            'change_reason': version.change_reason,
            'changed_by': version.changed_by.username if version.changed_by else None,
            'changed_at': version.changed_at,
        }
        return Response(data)
