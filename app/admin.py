from django.contrib import admin
from app.models import Cardapio


class Cardapios(admin.ModelAdmin):
    list_display = ('id', 'prato', 'preco', 'estoque', 'disponibilidade',)
    list_display_links = ('id', 'prato',)
    list_per_page = 20
    search_fields = ('prato',)


admin.site.register(Cardapio, Cardapios)
