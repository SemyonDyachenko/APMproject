from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Tournament)
admin.site.register(League)
admin.site.register(WeightClass)
admin.site.register(Match)
admin.site.register(Competitor)
admin.site.register(TournamentRegistration)
admin.site.register(TournamentWeightClasses)
admin.site.register(LeagueReview)
admin.site.register(TournamentReview)
admin.site.register(TournamentNotification)
admin.site.register(LeagueCompetitor)
admin.site.register(Team)
admin.site.register(TeamCompetitor)