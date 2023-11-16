from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import TournamentRegistration
from django.db.models import Q
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.decorators import action
from django.db.models import Avg
from django.http import JsonResponse

class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all().order_by('-elo_rating')
    serializer_class = CompetitorSerializer


class PropsUpdateViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = ProfileSerializer

    def update(self, request, *args, **kwargs):
        competitor_id = request.data.get('id',None)
        trainer = request.data.get('trainer',None)
        birthdate = request.data.get('birthdate',None)
        height = request.data.get('height',None)
        city =  request.data.get('city',None)
        weight =  request.data.get('weight',None)
        career_start_date = request.data.get('career_start_date',None)
        description = request.data.get('description',None)
        if competitor_id is not None:
            try:
                competitor = Competitor.objects.get(id=competitor_id)
                competitor.trainer = Competitor.objects.get(id=trainer)
                competitor.birthdate = birthdate
                competitor.height = height
                competitor.weight = weight
                competitor.description = description
                competitor.career_start_date = career_start_date
                competitor.city = city
                competitor.save()
                serializer = CompetitorSerializer(competitor)
                return Response(serializer.data)
            except Competitor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Competitor.objects.all()

    def update(self, request, *args, **kwargs):
        competitor_id = request.data.get('id',None)
        image = request.data.get('image',None)

        if competitor_id is not None and image is not None:
            try: 
                competitor = Competitor.objects.get(id=competitor_id)
                competitor.image = image
                competitor.save()
                serializer = CompetitorSerializer(competitor)
                return Response(serializer.data)
            except Competitor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Competitor.objects.all()

    def update(self, request, *args, **kwargs):
        competitor_id = request.data.get('id',None)
        firstname = request.data.get('firstname',None)
        lastname = request.data.get('lastname',None)
        country= request.data.get('country',None)
        phone = request.data.get('phone',None)
        if competitor_id is not None and phone is not None and firstname is not None and lastname is not None and country is not None:
            try:
                competitor = Competitor.objects.get(id=competitor_id)
                competitor.country = country
                competitor.last_name = lastname
                competitor.first_name = firstname
                competitor.phone = phone
                competitor.save()
                serializer = CompetitorSerializer(competitor)
                return Response(serializer.data)
            except Competitor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user.id
        queryset = Competitor.objects.filter(id=user)
        return queryset


class MatchListViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer

    def get_queryset(self):
        tournament_id = self.request.query_params.get('tournament_id', None)
        competitor_id = self.request.query_params.get('competitorId', None)
        if competitor_id is not None:
            competitor = Competitor.objects.get(id=competitor_id)
            queryset = Match.objects.filter(Q(first_competitor=competitor) | Q(second_competitor=competitor))
            return queryset
        if tournament_id is not None:
            tournament = Tournament.objects.get(id=tournament_id)
            queryset = Match.objects.filter(tournament=tournament)
            return queryset

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = TournamentSerializer
    

    def get_queryset(self):
        queryset = Tournament.objects.all()
        queryset = queryset.filter()
        league = self.request.query_params.get('league', None)
        active = self.request.query_params.get('active',None)
        organizer = self.request.query_params.get('organizer',None)

        if organizer is not None:
            organizerCompetitor = Competitor.objects.get(id=organizer)
            queryset = queryset.filter(organizer = organizerCompetitor)
        if league is not None:
            queryset = queryset.filter(league=league)
        if active is not None:
            queryset = queryset.filter(active=active)
            
        return queryset

class TournamentUpdateViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def update(self, request, *args, **kwargs):
        tournamentId = request.data.get('tournamentId')

        leagueId = request.data.get('league')
        league = League.objects.get(id=leagueId)
        description = request.data.get('description')
        date = request.data.get('date')
        city = request.data.get('city')
        phone = request.data.get('phone')
        level = request.data.get('level')
        judge = request.data.get('judge')
        main_referee = Competitor.objects.get(id=judge)
        secretaryId = request.data.get('secretary')
        secretary = Competitor.objects.get(id=secretaryId)
        name = request.data.get('name')
        print(request.data)
        print(tournamentId)
        print(name)
        if tournamentId is not None:   
            try:
                tournament = Tournament.objects.get(id=tournamentId)
                tournament.league = league
                tournament.name = name
                tournament.location = city
                tournament.phone = phone
                tournament.description = description
                tournament.date = date
                tournament.level = level
                tournament.main_referee = main_referee
                tournament.main_secretary = secretary
                tournament.save()
               
                serializer = TournamentSerializer(tournament)
                return Response(serializer.data)
            except Tournament.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class AvarageReviewsRatingTournament(viewsets.ModelViewSet):
    serializer_class = TournamentReviewSerializer
    queryset = TournamentReview.objects.all()

    def get_queryset(self):
        queryset = TournamentReview.objects.all()
        tournament_id = self.request.query_params.get('tournamentId',None)
        if tournament_id is not None:
            tournament = Tournament.objects.get(id=tournament_id)
            reviews = TournamentReview.objects.filter(tournament=tournament)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            print(average_rating)
            return [{'average_rating': average_rating}]
        else:
            return queryset

class TournamentDeleteViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()
    

    def destroy(self, request, *args, **kwargs):
        tournament_id = request.query_params.get('tournamentId', None)

        if tournament_id is not None:
            try:
                tournament = Tournament.objects.get(id=tournament_id)
                tournament.delete()
                return Response({"detail": "Tournament successfully deleted"}, status=status.HTTP_200_OK)
            except Tournament.DoesNotExist:
                return Response({"detail": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Invalid request. Provide 'tournamentId' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        


class WeightClassViewSet(viewsets.ModelViewSet):
    queryset = WeightClass.objects.all()
    serializer_class = WeightClassSerializer

class TournamentProtocolViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        tournament_id = request.data.get('tournamentId',None)
        activated = request.data.get('activated', None)
        if tournament_id is not None and activated is not None:
            try:
                tournament = Tournament.objects.get(id=tournament_id)
                tournament.is_started = activated
                tournament.save()
                serializer = TournamentSerializer(tournament)
                return Response(serializer.data)
            except Tournament.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TournamentsByCompetitorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TournamentSerializer  # Здесь используйте ваш сериализатор для модели Tournament

    def get_queryset(self):
        competitor_id = self.request.query_params.get('competitorId',None)
        return Tournament.objects.filter(tournamentregistration__competitor_id=competitor_id)
    

class TournamentCompetitors(viewsets.ReadOnlyModelViewSet):
   serializer_class = CompetitorSerializer

   def get_queryset(self):
    tournament_id = self.request.query_params.get('tournamentId',None)
    return Competitor.objects.filter(tournamentregistration__tournament_id=tournament_id)
   
class TournamentRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentRegistrationSerializer
    queryset = TournamentRegistration.objects.all()

    class Meta:
        model = TournamentRegistration
        fields = '__all__'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        tournament = request.data.get('tournament')
        competitor = request.data.get('competitor')
        weight_class = request.data.get('weight_class')
        category = request.data.get('category')

        try:
            tournament_obj = Tournament.objects.get(id=tournament)
            competitor_obj = Competitor.objects.get(id=competitor)
            weight_class_obj = WeightClass.objects.get(id=weight_class)
            
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except Competitor.DoesNotExist:
            return Response({'error': 'Competitor does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except WeightClass.DoesNotExist:
            return Response({'error': 'Weight Class does not exist.'},status=status.HTTP_400_BAD_REQUEST)

        if TournamentRegistration.objects.filter(tournament=tournament_obj, competitor=competitor_obj, weight_class=weight_class_obj).exists():
            return Response({'error': 'Tournament registration already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(tournament=tournament_obj, competitor=competitor_obj,weight_class=weight_class_obj,category=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        tournament_id = self.request.query_params.get('tournamentId', None)
        if tournament_id is not None:
            tournament = Tournament.objects.get(id=tournament_id)
            queryset = queryset.filter(tournament=tournament)
        else:
            return Response({'error': 'Registered Competitors for this tournament not found.'})
        return queryset

class TournamentWeightClassesViewSet(viewsets.ModelViewSet):
    queryset = TournamentWeightClasses.objects.all()  
    serializer_class = TournamentWeightClassesSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tournament_id = self.request.query_params.get('tournamentId', None)
        if tournament_id is not None:
            tournament = Tournament.objects.get(id=tournament_id)
            queryset = queryset.filter(tournament=tournament)

        return queryset

    class Meta:
        model = TournamentWeightClasses
        fields = '__all__'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        tournament = request.data.get('tournament')
        weightclass = request.data.get('weight_class')

        try:
            tournament_obj = Tournament.objects.get(id=tournament)
            weightclass_obj = WeightClass.objects.get(id=weightclass)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except WeightClass.DoesNotExist:
            return Response({'error': 'Weight class does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        if TournamentWeightClasses.objects.filter(tournament=tournament_obj, weight_class=weightclass_obj).exists():
            return Response({'error': 'Tournament weight class already added exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(tournament=tournament_obj, weight_class=weightclass_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        id = request.data.get('id', None)
        elo_rating = request.data.get('elo_rating', None)
        if id is not None and elo_rating is not None:
            try:
                competitor = Competitor.objects.get(id=id)
                competitor.elo_rating = elo_rating
                competitor.save()
                serializer = CompetitorSerializer(competitor)
                return Response(serializer.data)
            except Competitor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class TournamentReviewViewSet(viewsets.ModelViewSet):
    queryset = TournamentReview.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TournamentPOSTReviewSerializer
        return TournamentReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tournament_id = self.request.query_params.get('tournamentId', None)
        if tournament_id is not None:
            tournament = Tournament.objects.get(id=tournament_id)
            queryset = queryset.filter(tournament=tournament)

        return queryset
