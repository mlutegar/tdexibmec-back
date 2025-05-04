from django.db.models import Sum, Window, F
from django.db.models.functions import RowNumber
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pontuacao, Palestrante
from .serializers import PontuacaoSerializer


class PontuacaoCreateUpdateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        espectador = request.data.get('espectador')
        palestrante_id = request.data.get('palestrante')
        score_val = request.data.get('score')

        if not espectador:
            return Response(
                {'detail': 'O campo "espectador" é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if palestrante_id is None or score_val is None:
            return Response(
                {'detail': 'Você precisa enviar "palestrante" e "score".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Busca o palestrante
        try:
            palestrante = Palestrante.objects.get(pk=palestrante_id)
        except Palestrante.DoesNotExist:
            return Response(
                {'detail': 'Palestrante não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3) update_or_create pela dupla (espectador, palestrante)
        pontuacao, created = Pontuacao.objects.update_or_create(
            espectador=espectador,
            palestrante=palestrante,
            defaults={'score': score_val}
        )

        # 4) Serializa e retorna 201 se criou, 200 se atualizou
        serializer = PontuacaoSerializer(pontuacao)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class SpeakerRankingAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, speaker_id):
        # ranking de um palestrante específico
        qs = Pontuacao.objects.filter(palestrante_id=speaker_id) \
            .annotate(rank=Window(
                expression=RowNumber(),
                order_by=F('score').desc()
            ))
        data = [
            {
                'espectador': p.espectador,
                'score': p.score,
                'rank': p.rank
            } for p in qs
        ]
        return Response(data)


class OverallRankingAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # ranking geral (soma de todas as pontuações do espectador)
        agg = Pontuacao.objects.values('espectador') \
            .annotate(total_score=Sum('score')) \
            .order_by('-total_score')

        data = [
            {
                'espectador': a['espectador'],
                'total_score': a['total_score'],
                'rank': idx + 1
            } for idx, a in enumerate(agg)
        ]
        return Response(data)
