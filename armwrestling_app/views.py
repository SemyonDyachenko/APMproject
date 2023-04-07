from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all().order_by('-elo_rating')
    serializer_class = CompetitorSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user.id
        queryset = Competitor.objects.filter(id=user)
        return queryset


class MatchListViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer

    def get_queryset(self):
        tournament_id = self.request.query_params.get('tournament_id', None)
        tournament = Tournament.objects.get(id=tournament_id)
        print(tournament)
        queryset = Match.objects.filter(tournament=tournament)
        return queryset


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer


class WeightClassViewSet(viewsets.ModelViewSet):
    queryset = WeightClass.objects.all()
    serializer_class = WeightClassSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        id = request.data.get('id', None)
        elo_rating = request.data.get('elo_rating', None)
        if id is not None and elo_rating is not None:
            try:
                competitor = Competitor.objects.get(id=id)
                competitor.elo_rating = elo_rating
                competitor.save()
                serializer = CompetitorSerializer(competitor)
                return Response(serializer.data)
            except Competitor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)