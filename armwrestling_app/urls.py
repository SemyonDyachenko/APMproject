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
router.register(r'updateProfileStats',StatsUpdateViewSet,basename='updatestats')
router.register(r'updateProfileImage',ProfileImageViewSet,basename='updateprofileimage')
router.register(r'deleteCompetitorImage',ProfileImageDeleteViewSet,basename='deleteCompetitorImage')
router.register(r'tournamentCompetitors',TournamentCompetitors,basename='tournamentCompetitors')
router.register(r'competitorTournaments',TournamentsByCompetitorViewSet,basename='competitorTournaments')
router.register(r'tournamentReviews',TournamentReviewViewSet,basename='tournamentReviews')
router.register(r'leagueReviews',LeagueReviewViewSet,basename='leagueReviews')
router.register(r'deleteTournament',TournamentDeleteViewSet,basename='deleteTournament')
router.register(r'updateTournament',TournamentUpdateViewSet,basename='updateTournament')
router.register(r'averageTournamentReviews',AvarageReviewsRatingTournament,basename='avarageTournamentReviews')
router.register(r'averageLeagueReviews',AvarageReviewsRatingLeague,basename='averageLeagueReviews')
router.register(r'leagueByPresident',LeagueByPresidentViewSet,basename='leagueByPresident')
router.register(r'tournamentNotifications',TournamentNotificationViewSet,basename='tournamentNotifications')
router.register(r'tournamentNotificationCreate',TournamentNotificationCreateViewSet,basename='tournamentNoficationCreate')
router.register(r'tournamentActive',TournamentActiveViewSet,basename='tournamentActivate')
router.register(r'updateLeague',LeagueUpdateViewSet,basename='leagueUpdate')
router.register(r'leagueCompetitors',LeagueCompetitorsViewSet,basename='leagueCompetitors')
router.register(r'leagueCompetitorCreate',LeagueCompetitorCreate,basename='leagueCompetitorCreate')
router.register(r'leagueCompetitorAccept',LeagueCompetitorAccept,basename='leagueCompetitorAccept')
router.register(r'confirm',CompetitorConfirmViewSet,basename='confirm')
router.register(r'deleteLeague',LeagueDeleteViewSet,basename='leagueDelete')
router.register(r'leagueUpdateImages',LeagueUpdateImageViewSet,basename='leagueImagesUpdate')
router.register(r'teamUpdateImages',TeamUpdateImageViewSet,basename='teamImagesUpdate')
router.register(r'tournamentUpdateImage',TournamentUpdateImageViewSet,basename='tournamentUpdateImage')
router.register(r'createTournamentWeightClasses',TournamentWeightClassesCreateViewSet,basename='createTournamentWeightClass')
router.register(r'passwordRestore',PasswordRestoreViewSet,basename='passwordRestore')
router.register(r'supportRequest',SupportRequestViewSet,basename='supportRequest')
router.register(r'team',TeamViewSet,basename='team')
router.register(r'competitorTeams',TeamCompetitorViewSet,basename="teamCompetitor")
router.register(r'teamCompetitorAcceptt',TeamCompetitorAcceptViewSet,basename="teamCompetitorAccept")
router.register(r'updateCompetitorTeam',UpdateCompetitorTeamViewSet,basename='updateCompetitorTeam')
router.register(r'tournament_registration_confirm',TournamentRegistrationConfirmViewSet,basename='registration_confirm')
router.register(r'tournament_registration_delete',TournamentRegistrationDeleteViewSet,basename='registration_delete')
router.register(r'tournament_params',TournamentParamsViewSet,basename='tournamentParams')
router.register(r'league_image_delete',LeagueImageDeleteViewSet,basename='deleteLeagueImage')
urlpatterns = [
    path('', include(router.urls)),
    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
