from django.contrib import admin
from .models import ConfigVersion

@admin.register(ConfigVersion)
class ConfigVersionAdmin(admin.ModelAdmin):
    list_display = ('config', 'version', 'format', 'changed_by', 'changed_at')
    list_filter = ('format', 'changed_at')
    search_fields = ('config__name', 'change_reason')
    readonly_fields = ('config', 'version', 'format', 'content_text', 'parsed_data', 'change_reason', 'changed_by', 'changed_at')
