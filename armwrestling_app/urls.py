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
router.register(r'weightclasses',WeightClassViewSet, basename='weightclass')
router.register(r'tournament_registration',TournamentRegistrationViewSet,basename='tournamentregistration')
router.register(r'tournament_weightclasses',TournamentWeightClassesViewSet,basename='tournamentweightclass' )
router.register(r'startTournament',TournamentProtocolViewSet, basename='starttournament')
router.register(r'updateProfile',ProfileUpdateViewSet,basename='updateprofile')
router.register(r'updateProfileProps',PropsUpdateViewSet,basename='updateprops')
router.register(r'updateProfileImage',ProfileImageViewSet,basename='updateprofileimage')
router.register(r'tournamentCompetitors',TournamentCompetitors,basename='tournamentCompetitors')
router.register(r'competitorTournaments',TournamentsByCompetitorViewSet,basename='competitorTournaments')
router.register(r'tournamentReviews',TournamentReviewViewSet,basename='tournamentReviews')
router.register(r'deleteTournament',TournamentDeleteViewSet,basename='deleteTournament')
router.register(r'updateTournament',TournamentUpdateViewSet,basename='updateTournament')
router.register(r'averageTournamentReviews',AvarageReviewsRatingTournament,basename='avarageTournamentReviews')
urlpatterns = [
    path('', include(router.urls)),
    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]