from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Tournament)
admin.site.register(League)
admin.site.register(WeightClass)
admin.site.register(Match)
admin.site.register(Competitor)
admin.site.register(TournamentRegistration)