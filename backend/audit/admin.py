from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'resource_type', 'resource_name', 'created_at')
    list_filter = ('action', 'resource_type', 'created_at')
    search_fields = ('resource_name', 'user__username')
    readonly_fields = ('user', 'action', 'resource_type', 'resource_id', 'resource_name', 'details', 'ip_address', 'created_at')
    date_hierarchy = 'created_at'
