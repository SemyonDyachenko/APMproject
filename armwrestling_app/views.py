from rest_framework import viewsets
from .models import *
from .serializers import *


class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer

class LeagueViewSet(viewsets.ModelViewSet):

    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class WeightClassViewSet(viewsets.ModelViewSet):
    queryset = WeightClass.objects.all()
    serializer_class = WeightClassSerializer