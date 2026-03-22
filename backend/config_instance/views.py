from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import ConfigInstance
from .serializers import ConfigInstanceSerializer, ConfigInstanceListSerializer
from versioning.models import ConfigVersion
from audit.models import AuditLog


class ConfigInstanceViewSet(viewsets.ModelViewSet):
    """配置实例管理 API"""
    queryset = ConfigInstance.objects.all()
    serializer_class = ConfigInstanceSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConfigInstanceListSerializer
        return ConfigInstanceSerializer
    
    def get_queryset(self):
        queryset = ConfigInstance.objects.all()
        config_type = self.request.query_params.get('config_type', None)
        search = self.request.query_params.get('search', None)
        format_type = self.request.query_params.get('format', None)
        
        if config_type:
            queryset = queryset.filter(config_type__name=config_type)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if format_type:
            queryset = queryset.filter(format=format_type)
        
        return queryset.select_related('config_type')
    
    @transaction.atomic
    def perform_create(self, serializer):
        """创建时保存版本历史"""
        instance = serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)
        
        # 创建初始版本
        ConfigVersion.objects.create(
            config=instance,
            version=1,
            format=instance.format,
            content_text=instance.content_text,
            parsed_data=instance.parsed_data,
            change_reason='初始创建',
            changed_by=instance.created_by
        )
        
        # 记录审计日志
        AuditLog.objects.create(
            user=instance.created_by,
            action='CREATE',
            resource_type='ConfigInstance',
            resource_id=str(instance.id),
            resource_name=f"{instance.config_type.title}/{instance.name}",
            details={'format': instance.format}
        )
    
    @transaction.atomic
    def perform_update(self, serializer):
        """更新时保存版本历史"""
        instance = serializer.instance
        old_version = instance.version
        
        # 增加版本号
        serializer.save(version=old_version + 1)
        instance.refresh_from_db()
        
        # 创建新版本记录
        ConfigVersion.objects.create(
            config=instance,
            version=instance.version,
            format=instance.format,
            content_text=instance.content_text,
            parsed_data=instance.parsed_data,
            changed_by=self.request.user if self.request.user.is_authenticated else None
        )
        
        # 记录审计日志
        AuditLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action='UPDATE',
            resource_type='ConfigInstance',
            resource_id=str(instance.id),
            resource_name=f"{instance.config_type.title}/{instance.name}",
            details={'version': instance.version, 'old_version': old_version}
        )
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """获取配置版本历史"""
        instance = self.get_object()
        versions = instance.versions.all()
        data = [{
            'version': v.version,
            'format': v.format,
            'change_reason': v.change_reason,
            'changed_by': v.changed_by.username if v.changed_by else None,
            'changed_at': v.changed_at,
        } for v in versions]
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def rollback(self, request, pk=None):
        """回滚到指定版本"""
        instance = self.get_object()
        version_num = request.data.get('version')
        
        try:
            target_version = instance.versions.get(version=version_num)
        except ConfigVersion.DoesNotExist:
            return Response({'error': '版本不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        # 创建新版本（回滚内容）
        new_version = instance.version + 1
        instance.content_text = target_version.content_text
        instance.parsed_data = target_version.parsed_data
        instance.format = target_version.format
        instance.version = new_version
        instance.save()
        
        # 记录回滚版本
        ConfigVersion.objects.create(
            config=instance,
            version=new_version,
            format=instance.format,
            content_text=instance.content_text,
            parsed_data=instance.parsed_data,
            change_reason=f'回滚到版本 {version_num}',
            changed_by=request.user if request.user.is_authenticated else None
        )
        
        return Response({'message': f'已回滚到版本 {version_num}', 'new_version': new_version})
    
    @action(detail=True, methods=['get'])
    def content(self, request, pk=None):
        """获取指定格式的内容"""
        instance = self.get_object()
        output_format = request.query_params.get('format', instance.format)
        
        content = instance.get_content_by_format(output_format)
        return Response({
            'format': output_format,
            'content': content,
            'parsed_data': instance.parsed_data
        })
