from django.urls import path
from .views import (
    PontuacaoCreateUpdateAPIView,
    SpeakerRankingAPIView,
    OverallRankingAPIView
)

urlpatterns = [
    path('api/scores/', PontuacaoCreateUpdateAPIView.as_view(), name='submit-score'),
    path('api/rankings/speaker/<int:speaker_id>/', SpeakerRankingAPIView.as_view(), name='speaker-ranking'),
    path('api/rankings/overall/', OverallRankingAPIView.as_view(), name='overall-ranking'),
]
