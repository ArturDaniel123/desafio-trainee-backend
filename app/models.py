from django.db import models
from django.contrib.auth.models import User


class Cardapio(models.Model):
    '''Representa os pratos disponíveis no restaurante'''
    prato = models.CharField(max_length=100, unique=True)  # Nome do prato
    # Preço com duas casas decimais
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    estoque = models.PositiveIntegerField()  # Quantidade disponível em estoque
    # Indica se o prato está disponível para compra
    disponibilidade = models.BooleanField(default=True)

    def __str__(self):
        return self.prato


class Pedido(models.Model):
    '''Pedido feito por um cliente'''
    cliente = models.ForeignKey(
        User, on_delete=models.CASCADE)  # Cliente que fez o pedido

    # Data e hora em que o pedido foi criado
    data = models.DateTimeField(auto_now_add=True)

    # Indica se o pedido já foi finalizado
    finalizado = models.BooleanField(default=False)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, related_name='itens', on_delete=models.CASCADE)
    prato = models.ForeignKey('Cardapio', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()


class MetodoPagamento(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome
