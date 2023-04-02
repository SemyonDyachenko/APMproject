from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'competitors', CompetitorViewSet, basename='competitor')
router.register(r'competitor', ProfileViewSet,basename='profile')
router.register(r'leagues', LeagueViewSet, basename='league')
router.register(r'matches', MatchViewSet,basename='match')
router.register(r'matcheslist', MatchListViewSet,basename='matchlist')
router.register(r'updaterating', RatingViewSet,basename='rating')
router.register(r'tournaments', TournamentViewSet,basename='tournament')
router.register(r'weights',WeightClassViewSet, basename='weightclass')

urlpatterns = [
    path('', include(router.urls)),
    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]