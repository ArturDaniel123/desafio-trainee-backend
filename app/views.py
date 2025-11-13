from app.models import Cardapio
from app.serializers import CardapioSerializer
from rest_framework import viewsets


class CardapioViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer
