from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('ragione_sociale', 'citta', 'piva')
    search_fields = ('ragione_sociale', 'citta', 'piva')
