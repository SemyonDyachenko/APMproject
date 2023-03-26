from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'competitors', CompetitorViewSet, basename='competitor')
router.register(r'leagues', LeagueViewSet, basename='league')
router.register(r'matches', MatchViewSet,basename='match')
router.register(r'tournaments', TournamentViewSet,basename='tournament')
router.register(r'weights',WeightClassViewSet, basename='weightclass')
urlpatterns = router.urls