from django.db import models


class Cardapio(models.Model):
    prato = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    estoque = models.PositiveIntegerField()
    disponibilidade = models.BooleanField(default=True)

    def __str__(self):
        return self.prato


'''
EXISTE UM EMAILFIELD PARA QUANDO EU FOR CRIAR O CADASTRO
'''
