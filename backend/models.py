from django.db import models


class Espectador(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
