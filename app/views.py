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


class CardapioViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class RegistroViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({'mensagem': 'Login efetuado com sucesso!'}, status=status.HTTP_200_OK)
        else:
            return Response({'erro': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({'mensagem': 'Login efetuado'}, status=status.HTTP_200_OK)
        else:
            return Response({'erro': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pedido.objects.all()  # Admin vê todos os pedidos
        # Usuário vê apenas os próprios
        return Pedido.objects.filter(cliente=user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    @action(detail=True, methods=['post'])
    def adicionar_item(self, request, pk=None):
        pedido = self.get_object()
        prato_id = request.data.get('prato')
        quantidade = int(request.data.get('quantidade', 1))

        try:
            prato = Cardapio.objects.get(id=prato_id)
        except Cardapio.DoesNotExist:
            return Response({'erro': 'Prato não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if prato.estoque < quantidade:
            return Response({'erro': f'Estoque insuficiente. Disponível: {prato.estoque}'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Atualiza estoque
        prato.estoque -= quantidade
        prato.save()

        # Cria ou atualiza item no pedido
        item, created = ItemPedido.objects.get_or_create(
            pedido=pedido, prato=prato,
            defaults={'quantidade': quantidade}
        )
        if not created:
            item.quantidade += quantidade
            item.save()

        return Response({'mensagem': f'{quantidade} x {prato.prato} adicionado ao pedido.'})
