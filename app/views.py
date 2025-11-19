from app.models import Cardapio, Pedido, ItemPedido
from app.serializers import CardapioSerializer, PedidoSerializer, ItemPedidoSerializer
from rest_framework import viewsets, status, permissions
from django.contrib.auth.models import User
from app.serializers import RegistroSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import BasicAuthentication
from rest_framework import mixins, serializers
from django.utils.dateparse import parse_datetime
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from rest_framework.viewsets import ModelViewSet


class CardapioViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class RegistroViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def teste(self, request):
        return Response({'msg': 'rota funcionando'})

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            return Response({'mensagem': 'Login efetuado com sucesso!'})
        return Response({'erro': 'Credenciais inválidas.'}, status=401)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pedido.objects.all()
        return Pedido.objects.filter(cliente=user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    # ---------------------------
    #  ADICIONAR ITEM AO PEDIDO
    # ---------------------------
    @action(detail=True, methods=['post'])
    def adicionar_item(self, request, pk=None):
        pedido = self.get_object()
        prato_nome = request.data.get('prato')
        quantidade = int(request.data.get('quantidade', 1))

        try:
            prato = Cardapio.objects.get(prato__iexact=prato_nome)
        except Cardapio.DoesNotExist:
            return Response({'erro': f'Prato "{prato_nome}" não encontrado.'}, status=404)

        if quantidade <= 0:
            return Response({'erro': 'Quantidade inválida'}, status=400)

        if prato.estoque < quantidade:
            return Response(
                {'erro': f'Estoque insuficiente. Disponível: {prato.estoque}'},
                status=400
            )

        item, created = ItemPedido.objects.get_or_create(
            pedido=pedido,
            prato=prato,
            defaults={'quantidade': quantidade}
        )

        if not created:
            item.quantidade += quantidade
            item.save()

        return Response({'mensagem': f'{quantidade} x {prato.prato} adicionado ao pedido.'})

    # ---------------------------
    #  FINALIZAR O PEDIDO
    # ---------------------------
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        pedido = self.get_object()

        if pedido.finalizado:
            return Response({'erro': 'Pedido já finalizado'}, status=400)

        for item in pedido.itens.all():
            if item.quantidade > item.prato.estoque:
                return Response({'erro': f'Estoque insuficiente para {item.prato.prato}'}, status=400)

        for item in pedido.itens.all():
            prato = item.prato
            prato.estoque -= item.quantidade
            prato.save()

        pedido.finalizado = True
        pedido.save()

        return Response({'mensagem': 'Pedido finalizado com sucesso!'})

    # (OPCIONAL) faturamento dentro do ViewSet para ADM


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def faturamento(request):
    data_inicio = request.query_params.get('inicio')
    data_fim = request.query_params.get('fim')

    if not data_inicio or not data_fim:
        return Response({"erro": "Envie ?inicio=AAAA-MM-DD&fim=AAAA-MM-DD"})

    pedidos = Pedido.objects.filter(
        finalizado=True,
        data__date__range=[data_inicio, data_fim]
    )

    total = 0
    for pedido in pedidos:
        for item in pedido.itens.all():
            total += item.quantidade * item.prato.preco

    return Response({
        "faturamento_total": total,
        "periodo": f"{data_inicio} a {data_fim}",
        "pedidos_considerados": pedidos.count()
    })


class AdicionarItemSerializer(serializers.Serializer):
    prato = serializers.CharField()
    quantidade = serializers.IntegerField()
