from rest_framework import serializers
from app.models import Cardapio, Pedido, ItemPedido, MetodoPagamento
from django.contrib.auth.models import User


class CardapioSerializer(serializers.ModelSerializer):
    '''Serializador do cardápio'''
    class Meta:
        model = Cardapio
        fields = ['id', 'prato', 'preco', 'estoque', 'disponibilidade']

    def validate_prato(self, value):
        '''Impede pratos com mesmo nome'''
        if Cardapio.objects.filter(prato__iexact=value).exists():
            raise serializers.ValidationError(
                "Já existe um prato com esse nome.")
        return value


class RegistroSerializer(serializers.ModelSerializer):
    '''Serializador para criação de usuários'''
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        '''Impede e-mails repetidos'''
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return value

    def create(self, validated_data):
        '''Criação segura do usuário com hash de senha'''
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class ItemPedidoSerializer(serializers.ModelSerializer):
    prato = serializers.SlugRelatedField(
        slug_field='prato',              # vai buscar o Cardapio pelo nome
        queryset=Cardapio.objects.all()  # habilita escrita (não apenas leitura)
    )
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

    def get_total_itens(self, obj):
        return sum(item.quantidade for item in obj.itens.all())

    def get_total_valor(self, obj):
        return sum(item.quantidade * item.prato.preco for item in obj.itens.all())


class MetodoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPagamento
        fields = '__all__'
