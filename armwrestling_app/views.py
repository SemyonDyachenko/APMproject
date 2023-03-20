from rest_framework import viewsets
from .models import Competitor
from .serializers import CompetitorSerializer


class CompetitorViewSet(viewsets.ModelViewSet):

    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer