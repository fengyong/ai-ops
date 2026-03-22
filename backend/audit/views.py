from rest_framework import viewsets
from rest_framework.response import Response
from .models import AuditLog


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """审计日志管理 API"""
    queryset = AuditLog.objects.all().order_by('-created_at')
    
    def list(self, request):
        """获取审计日志列表"""
        resource_type = request.query_params.get('resource_type')
        action = request.query_params.get('action')
        user_id = request.query_params.get('user_id')
        
        queryset = AuditLog.objects.all()
        
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        if action:
            queryset = queryset.filter(action=action)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        data = [{
            'id': log.id,
            'user': log.user.username if log.user else None,
            'action': log.action,
            'resource_type': log.resource_type,
            'resource_id': log.resource_id,
            'resource_name': log.resource_name,
            'details': log.details,
            'timestamp': log.created_at,
        } for log in queryset.order_by('-created_at')]
        
        return Response(data)
    
    def retrieve(self, request, pk=None):
        """获取单个审计日志详情"""
        log = self.get_object()
        data = {
            'id': log.id,
            'user': log.user.username if log.user else None,
            'action': log.action,
            'resource_type': log.resource_type,
            'resource_id': log.resource_id,
            'resource_name': log.resource_name,
            'details': log.details,
            'timestamp': log.created_at,
        }
        return Response(data)
