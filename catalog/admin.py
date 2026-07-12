from django.contrib import admin

from .models import AppLink


@admin.register(AppLink)
class AppLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
