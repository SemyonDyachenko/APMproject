from django.contrib import admin
from .models import Tournament,League,WeightClass,Match,Competitor
# Register your models here.

admin.site.register(Tournament)
admin.site.register(League)
admin.site.register(WeightClass)
admin.site.register(Match)
admin.site.register(Competitor)
