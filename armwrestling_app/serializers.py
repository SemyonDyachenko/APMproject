from rest_framework import serializers
from .models import Competitor

class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = ['id','first_name','last_name','gender','elo_rating']