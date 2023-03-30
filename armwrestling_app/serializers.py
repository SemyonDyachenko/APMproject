from rest_framework import serializers
from .models import Competitor, League, Match, Tournament, WeightClass

class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = ['id', 'first_name', 'last_name', 'gender', 'elo_rating']

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competitor
        fields = '__all__'

class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = '__all__'

class TournamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = '__all__'

class WeightClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeightClass
        fields = '__all__'