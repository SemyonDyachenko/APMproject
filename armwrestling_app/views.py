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
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import  redirect

def generate_token():
    import secrets
    return secrets.token_urlsafe(30)

def send_confirmation_email(user, token):
    subject = 'Подтверждение регистрации'
    message = f'Пожалуйста, перейдите по ссылке для подтверждения: http://127.0.0.1:8000/api/confirm/?token={token}'
    from_email = 'semyondyachenko@gmail.com'  # Замените на ваш адрес электронной почты
    to_email = user.email

    send_mail(subject, message, from_email, [to_email])

class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.filter(verified=True).order_by('-elo_rating')
    serializer_class = CompetitorSerializer

    @action(detail=True, methods=['GET'])
    def rating_position(self, request, pk=None):
        competitor = self.get_object()
        rating_queryset = Competitor.objects.filter(verified=True).order_by('-elo_rating')
        rating_list = list(rating_queryset.values_list('id', flat=True))
        position = rating_list.index(competitor.id) + 1

        return Response({'rating_position': position})


    def perform_create(self, serializer):
        instance = serializer.save(token=generate_token())
        send_confirmation_email(instance, instance.token)


class CompetitorConfirmViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        token = self.request.query_params.get('token')
        
        if token is not None:
            try:
                competitor = Competitor.objects.get(token=token)
                competitor.verified = True
                competitor.save()
                # Вернем редирект
                return Response(status=status.HTTP_302_FOUND, headers={'Location': 'http://localhost:5173/profile'})
            except Competitor.DoesNotExist:
                pass

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

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
        


class StatsUpdateViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = ProfileSerializer

    def update(self, request, *args, **kwargs):
        competitor_id = request.data.get('id',None)
        grip = request.data.get('grip',None)
        biceps = request.data.get('biceps',None)
        crossbar = request.data.get('crossbar',None)
        shaft =  request.data.get('shaft',None)
        militarypress =  request.data.get('militarypress',None)
        hand = request.data.get('hand',None)
        press = request.data.get('press',None)
        side = request.data.get('side',None)
        if competitor_id is not None:
            try:
                competitor = Competitor.objects.get(id=competitor_id)
                competitor.grip = grip
                competitor.biceps = biceps
                competitor.shaft = shaft
                competitor.crossbar = crossbar
                competitor.militarypress = militarypress
                competitor.hand = hand
                competitor.press = press
                competitor.side = side
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

class ProfileImageDeleteViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Competitor.objects.all()

    def update(self, request, *args, **kwargs):
        competitor_id = request.data.get('id',None)

        if competitor_id is not None:
            try: 
                competitor = Competitor.objects.get(id=competitor_id)
                competitor.image = None
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




class LeagueDeleteViewSet(viewsets.ModelViewSet):
    serializer_class = LeagueSerializer
    queryset = League.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        league_id = request.query_params.get('leagueId', None)
        competitor_id = request.query_params.get('competitorId',None)
        if league_id is not None and competitor_id is not None:
            try:
                league = League.objects.get(id=league_id)
                competitor = Competitor.objects.get(id=competitor_id)
                if league.president == competitor:
                    league.delete()
                return Response({"detail": "League successfully deleted"}, status=status.HTTP_200_OK)
            except League.DoesNotExist:
                return Response({"detail": "League not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Invalid request. Provide 'tournamentId' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        



class LeagueUpdateViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    def update(self, request, *args, **kwargs):
        leagueId = request.data.get('leagueId')
    
        description = request.data.get('description')
        creation_date = request.data.get('creation_date')
        email = request.data.get('email')
        phone = request.data.get('phone')
        level = request.data.get('level')
        country = request.data.get('country')
        name = request.data.get('name')
    
        if leagueId is not None:   
            try:
                league = League.objects.get(id=leagueId)
                league.name = name
                league.country = country
                league.phone = phone
                league.email = email
                league.description = description
                league.creation_date = creation_date
                league.level = level
                league.save()
               
                serializer = LeagueSerializer(league)
                return Response(serializer.data)
            except League.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LeagueUpdateImageViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    def update(self, request, *args, **kwargs):
        leagueId = request.data.get('leagueId')
        banner = request.data.get('banner',None)
        logo = request.data.get('logo',None)

        if leagueId is not None:   
            try:
                league = League.objects.get(id=leagueId)
                
                if banner is not None:
                    league.banner = banner
                if logo is not None:
                    league.logo = logo
                league.save()
                serializer = LeagueSerializer(league)
                return Response(serializer.data)
            except League.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LeagueCompetitorsViewSet(viewsets.ModelViewSet):
    queryset = LeagueCompetitor.objects.all()
    serializer_class = LeagueCompetitorSerializer


    def get_queryset(self):
        leagueId = self.request.query_params.get('leagueId',None)
        competitorId =self.request.query_params.get('competitorId',None)

        queryset = super().get_queryset()
        
        if competitorId is not None:
            competitor = Competitor.objects.get(id=competitorId)
            if competitor is not None:
                queryset = queryset.filter(competitor=competitor)
         
        if leagueId is not None:
            league = League.objects.get(id=leagueId)
            if league is not None:
                queryset = queryset.filter(league=league)
        return queryset
    

class LeagueCompetitorCreate(viewsets.ModelViewSet):
    serializer_class = LeagueCompetitorPOSTSerializer
    queryset = LeagueCompetitor.objects.all()

class LeagueCompetitorAccept(viewsets.ModelViewSet):
    serializer_class = LeagueCompetitorSerializer
    queryset = LeagueCompetitor.objects.all() 
    
    def update(self, request, *args, **kwargs):
        competitorId = request.data.get('competitorId')
        if competitorId is not None:   
            try:
                competitor = LeagueCompetitor.objects.get(id=competitorId)
                competitor.accepted = True
                competitor.save()
                serializer = LeagueCompetitorSerializer(competitor)
                return Response(serializer.data)
            except LeagueCompetitor.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

class LeagueByPresidentViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    def get_queryset(self):
        queryset = League.objects.all()
        presidentId = self.request.query_params.get('presidentId',None)

        if presidentId is not None: 
            president = Competitor.objects.get(id=presidentId)
            queryset = queryset.filter(president=president)
        return queryset


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


class TournamentUpdateImageViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def update(self, request, *args, **kwargs):
        tournamentId = request.data.get('tournamentId')
        banner = request.data.get('banner',None)
        logo = request.data.get('logo',None)

        if tournamentId is not None:   
            try:
                tournament = Tournament.objects.get(id=tournamentId)
                
                if banner is not None:
                    tournament.banner = banner
                if logo is not None:
                    tournament.logo = logo
                tournament.save()
                serializer = TournamentSerializer(tournament)
                return Response(serializer.data)
            except Tournament.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class TournamentActiveViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def update(self, request, *args, **kwargs):
        tournamentId = request.data.get('tournamentId')
        if tournamentId is not None:   
            try:
                tournament = Tournament.objects.get(id=tournamentId)
                tournament.active = True
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

    @action(detail=False, methods=['GET'])
    def get_avarage(self, request):
        tournament_id = request.query_params.get('tournamentId', None)
        if tournament_id is not None:
            reviews = TournamentReview.objects.filter(tournament__id=tournament_id)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            print(average_rating)
            return Response({'average_rating': average_rating})
        else:
            return Response({'error': 'Please provide a tournamentId parameter'})

class AvarageReviewsRatingLeague(viewsets.ModelViewSet):
    serializer_class = LeagueReviewSerializer
    queryset = LeagueReview.objects.all()

    @action(detail=False, methods=['GET'])
    def get_avarage(self, request):
        league_id = request.query_params.get('leagueId', None)
        if league_id is not None:
            reviews = LeagueReview.objects.filter(league__id=league_id)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            print(average_rating)
            return Response({'average_rating': average_rating})
        else:
            return Response({'error': 'Please provide a tournamentId parameter'})


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
    

class LeagueReviewViewSet(viewsets.ModelViewSet):
    queryset = LeagueReview.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LeaguePOSTReviewSerializer
        return LeagueReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        league_id = self.request.query_params.get('leagueId', None)
        if league_id is not None:
            league = League.objects.get(id=league_id)
            queryset = queryset.filter(league=league)

        return queryset

class TournamentNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentNotificationSerializer
    queryset = TournamentNotification.objects.all()

    def get_queryset(self):
        competitorId = self.request.query_params.get('competitorId',None)
        if competitorId is not None:
            competitor = Competitor.objects.get(id=competitorId)
            queryset = TournamentNotification.objects.filter(competitor=competitor)
            return queryset


class TournamentNotificationCreateViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentNotificationCreateSerializer
    queryset = TournamentNotification.objects.all()
    