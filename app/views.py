from app.models import Cardapio
from app.serializers import CardapioSerializer
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from app.serializers import RegistroSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import action


class CardapioViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer


class RegistroViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistroSerializer

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
