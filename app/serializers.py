from rest_framework import serializers
from app.models import Cardapio
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
