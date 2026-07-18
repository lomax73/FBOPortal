from django.contrib import admin

from .models import ElementoRack, Posizione, Rack, RackAllegato, Progetto


class RackInline(admin.TabularInline):
    model = Rack
    extra = 0


@admin.register(Progetto)
class ProgettoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cliente', 'sito', 'data_intervento')
    search_fields = ('nome', 'sito', 'cliente__ragione_sociale')
    inlines = [RackInline]


class ElementoRackInline(admin.TabularInline):
    model = ElementoRack
    extra = 0


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('nome', 'progetto', 'ordine')
    inlines = [ElementoRackInline]


class PosizioneInline(admin.TabularInline):
    model = Posizione
    extra = 0


@admin.register(ElementoRack)
class ElementoRackAdmin(admin.ModelAdmin):
    list_display = ('etichetta', 'tipo', 'rack', 'n_posizioni')
    inlines = [PosizioneInline]


@admin.register(RackAllegato)
class RackAllegatoAdmin(admin.ModelAdmin):
    list_display = ('nome_originale', 'rack', 'caricato_il')
