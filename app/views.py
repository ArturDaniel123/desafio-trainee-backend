from app.models import Cardapio
from app.serializers import CardapioSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from app.serializers import RegistroSerializer


class CardapioViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer


class RegistroViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistroSerializer
