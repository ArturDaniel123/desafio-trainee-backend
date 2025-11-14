from rest_framework import serializers
from app.models import Cardapio, Pedido, ItemPedido
from django.contrib.auth.models import User


class CardapioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardapio
        fields = ['id', 'prato', 'preco', 'estoque', 'disponibilidade']


class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class ItemPedidoSerializer(serializers.ModelSerializer):
    prato_nome = serializers.CharField(source='prato.prato', read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'prato', 'prato_nome', 'quantidade']


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    total_itens = serializers.SerializerMethodField()
    total_valor = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'data', 'finalizado',
                  'itens', 'total_itens', 'total_valor']

    def get_total_valor(self, obj):
        return sum(item.quantidade * item.prato.preco for item in obj.itens.all())
