from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class CompetitorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    kFactor = serializers.IntegerField(read_only=True)


    class Meta:
        model = Competitor
        fields = ['id', 'email', 'mode', 'first_name', 'last_name', 'gender', 'country','trainer', 'elo_rating', 'password', 'kFactor','weight','rank','image','description','height','city','birthdate','career_start_date']

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
    class Meta:
        model = Tournament
        fields = '__all__'


class TournamentNotificationSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()
    competitor = CompetitorSerializer()

    class Meta:
        model = TournamentNotification
        fields = '__all__'



class WeightClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeightClass
        fields = '__all__'

class TournamentReviewSerializer(serializers.ModelSerializer):
    author = CompetitorSerializer()
    class Meta:
        model = TournamentReview
        fields = '__all__'

class TournamentPOSTReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentReview
        fields = '__all__'

class LeagueReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeagueReview
        fields = '__all__'

class TournamentWeightClassesSerializer(serializers.ModelSerializer):
    weight_class = WeightClassSerializer()
    class Meta:
        model = TournamentWeightClasses
        fields = ['id', 'tournament', 'weight_class']

class TournamentRegistrationSerializer(serializers.ModelSerializer):
    competitor = CompetitorSerializer()
    weight_class = WeightClassSerializer()

    class Meta:
        model = TournamentRegistration
        fields = '__all__'
        read_only_fields = ['id']

