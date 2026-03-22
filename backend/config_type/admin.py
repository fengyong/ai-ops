from django.contrib import admin
from .models import ConfigType

@admin.register(ConfigType)
class ConfigTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'format', 'created_at')
    list_filter = ('format', 'created_at')
    search_fields = ('name', 'title')
    readonly_fields = ('created_at', 'updated_at')
