from django.contrib import admin
from .models import ConfigInstance

@admin.register(ConfigInstance)
class ConfigInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'config_type', 'format', 'version', 'created_at')
    list_filter = ('format', 'config_type', 'created_at')
    search_fields = ('name', 'config_type__name')
    readonly_fields = ('created_at', 'updated_at', 'parsed_data')
    fieldsets = (
        ('Basic', {'fields': ('config_type', 'name', 'format')}),
        ('Content', {'fields': ('content_text', 'parsed_data')}),
        ('Metadata', {'fields': ('version', 'created_by', 'created_at', 'updated_at')}),
    )
