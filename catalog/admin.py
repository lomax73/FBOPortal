from django.contrib import admin

from .models import AppLink


@admin.register(AppLink)
class AppLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'is_active', 'user_management_enabled')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'url', 'icon', 'order', 'is_active')}),
        ('Gestione utenti da remoto', {
            'fields': ('internal_base_url', 'api_token'),
            'description': 'Compilare entrambi solo per le app che espongono accounts/api/internal/ '
                           '(vedi deploy/README.md di quell\'app).',
        }),
    )
