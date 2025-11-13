from rest_framework import serializers
from app.models import Cardapio


class CardapioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardapio
        fields = ['id', 'prato', 'preco', 'estoque', 'disponibilidade']
