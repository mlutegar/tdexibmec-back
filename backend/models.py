from django.db import models


class Palestrante(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Espectador(models.Model):
    nome = models.CharField(max_length=50)
    avatar = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Pontuacao(models.Model):
    espectador = models.ForeignKey(Espectador, on_delete=models.CASCADE)
    palestrante = models.ForeignKey(Palestrante, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('espectador', 'palestrante')
        ordering = ['-score']

    def __str__(self):
        return f'{self.espectador} – {self.palestrante}: {self.score}'