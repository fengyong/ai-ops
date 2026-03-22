from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ConfigType
from .serializers import ConfigTypeSerializer


class ConfigTypeViewSet(viewsets.ModelViewSet):
    """配置类型管理 API"""
    queryset = ConfigType.objects.all()
    serializer_class = ConfigTypeSerializer
    lookup_field = 'name'
    
    def get_queryset(self):
        queryset = ConfigType.objects.all()
        search = self.request.query_params.get('search', None)
        format_type = self.request.query_params.get('format', None)
        
        if search:
            queryset = queryset.filter(name__icontains=search) | \
                      queryset.filter(title__icontains=search)
        if format_type:
            queryset = queryset.filter(format=format_type)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def instances(self, request, name=None):
        """获取该类型下的所有配置实例"""
        config_type = self.get_object()
        instances = config_type.configinstance_set.all()
        data = [{
            'id': inst.id,
            'name': inst.name,
            'version': inst.version,
            'updated_at': inst.updated_at,
        } for inst in instances]
        return Response(data)
