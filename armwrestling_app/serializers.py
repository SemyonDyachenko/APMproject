from rest_framework import serializers
from .models import Competitor, League, Match, Tournament, WeightClass
from django.contrib.auth.hashers import make_password


class CompetitorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    kFactor = serializers.IntegerField(read_only=True)


    class Meta:
        model = Competitor
        fields = ['id', 'email', 'mode', 'first_name', 'last_name', 'gender', 'elo_rating', 'password', 'kFactor']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)

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
    photo = serializers.ImageField()


    class Meta:
        model = Tournament
        fields = '__all__'

class WeightClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeightClass
        fields = '__all__'