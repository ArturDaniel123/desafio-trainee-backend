from django.contrib import admin
from app.models import Cardapio


class Cardapios(admin.ModelAdmin):
    list_display = ('id', 'prato', 'preco', 'estoque', 'disponibilidade')
    list_display_links =
    list_per_page
    search_fields
