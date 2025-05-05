from rest_framework import serializers
from .models import Pontuacao, Palestrante


class PontuacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pontuacao
        fields = ('espectador', 'palestrante', 'score')


class PalestranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palestrante
        fields = ('id', 'nome')
