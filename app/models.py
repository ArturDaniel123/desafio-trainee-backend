from django.db import models
from django.contrib.auth.models import User


class Cardapio(models.Model):
    prato = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    estoque = models.PositiveIntegerField()
    disponibilidade = models.BooleanField(default=True)

    def __str__(self):
        return self.prato


class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, related_name='itens', on_delete=models.CASCADE)
    prato = models.ForeignKey('Cardapio', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
