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
from django.shortcuts import  get_object_or_404, redirect
from django.contrib.auth import update_session_auth_hash
import string
import secrets 
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def generate_token():
    return secrets.token_urlsafe(30)

def send_confirmation_email(user, token):
    subject = 'Подтверждение регистрации'
    html_message = render_to_string('confirmation_email_template.html', {'token': token, 'server_url': 'http://localhost:5173' if settings.DEBUG else 'https://apm-league.ru'})
    plain_message = strip_tags(html_message)
    from_email = 'Armwrestling.promotion.machine@gmail.com'  # Replace with your email address
    to_email = user.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

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

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        competitorId = request.data.get('competitorId',None)
        current_password = request.data.get('current_password', '')
        new_password = request.data.get('new_password', '')

        # Проверка текущего пароля
        if competitorId is not None:
            competitor = Competitor.objects.get(id=competitorId)

            if not competitor.check_password(current_password):
                return Response({'detail': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        # Установка нового пароля
            competitor.set_password(new_password)
            competitor.save()

        # Обновление сессии с новым хешем пароля
        update_session_auth_hash(request, competitor)

        return Response({'detail': 'Password successfully updated.'}, status=status.HTTP_200_OK)

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
                return Response(status=status.HTTP_302_FOUND, headers={'Location': 'https://apm-league.ru/'})
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
                if trainer is not None:
                    existsTrainer = Competitor.objects.filter(id=trainer)
                    if existsTrainer.exists():
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


class UpdateCompetitorTeamViewSet(viewsets.ModelViewSet):
    serializer_class = CompetitorViewSet

    def update(self, request, *args, **kwargs):
        competitorId = request.data.get('competitorId')
        teamId = request.data.get('teamId')
        if competitorId is not None and teamId is not None:
            existsCompetitor = Competitor.objects.filter(id=competitorId)
            existsTeam = Team.objects.filter(id=teamId)
            if existsCompetitor.exists() and existsTeam.exists():
                competitor_obj = Competitor.objects.get(id=competitorId)
                team_obj = Team.objects.get(id=teamId)
                competitor_obj.team = team_obj
                competitor_obj.save()
                serializer = CompetitorSerializer(competitor_obj)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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




class TeamUpdateImageViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamPOSTSerializer

    def update(self, request, *args, **kwargs):
        teamId = request.data.get('teamId')
        banner = request.data.get('banner',None)
        logo = request.data.get('logo',None)

        if teamId is not None:   
            try:
                team = Team.objects.get(id=teamId)
                
                if banner is not None:
                    team.banner = banner
                if logo is not None:
                    team.logo = logo
                team.save()
                serializer = TeamPOSTSerializer(team)
                return Response(serializer.data)
            except Team.DoesNotExist:
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
        status = request.data.get("status")
        if competitorId is not None:   
            try:
                competitor = LeagueCompetitor.objects.get(id=competitorId)
                if status == "accepted":
                    competitor.accepted = True
                competitor.status = status
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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MatchPOSTSerializer
        return MatchSerializer
    

    @action(detail=False, methods=['post'])
    def remove_matches_of_category(self,request):
        tournamentId = request.data.get('tournamentId')
        hand = request.data.get('hand')
        weight_classId = request.data.get('weight_classId')
        category = request.data.get('category')

        if tournamentId is not None and weight_classId is not None:
            try:
                tournament = Tournament.objects.get(id=tournamentId)
                weightClass = WeightClass.objects.get(id=weight_classId)

                matches = Match.objects.filter(tournament=tournament,hand=hand,weight_class=weightClass,category=category)
                matches.delete()
                return Response({"detail": "Match successfully deleted"}, status=status.HTTP_200_OK)
            except Tournament.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message": "not find tournament"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message": "Not find"})
        

    def update(self, request, *args, **kwargs):
        winnerId = request.data.get('winner')
        matchId = request.data.get('matchId')
        first_new_rating = request.data.get('first_new_rating')
        second_new_rating = request.data.get('second_new_rating')

        if matchId is not None and winnerId is not None:
            try:
                match = Match.objects.get(id=matchId)
                try:
                    winner = Competitor.objects.get(id=winnerId)
                    match.winner = winner
                    match.first_competitor_result_rating = first_new_rating
                    match.second_competitor_result_rating = second_new_rating
                    match.save()
                    serializer = MatchSerializer(match)
                    
                    try:
                        firstCompetitor = Competitor.objects.get(id=match.first_competitor.id)
                        secondCompetitor = Competitor.objects.get(id=match.second_competitor.id)

                        if match.hand == 'left':
                            firstCompetitor.elo_rating = first_new_rating
                            secondCompetitor.elo_rating = second_new_rating
                        else:
                            firstCompetitor.elo_rating_right = first_new_rating
                            secondCompetitor.elo_rating_right = second_new_rating
                        
                        firstCompetitor.save()
                        secondCompetitor.save()
                        return Response(data=serializer.data)
                    except Competitor.DoesNotExist:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except Competitor.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except Match.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'match by id not found'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'match by id not found'})
                

    def create(self, request, *args, **kwargs):
        tournamentId = request.data.get('tournament')
        first_competitorId = request.data.get('first_competitor')
        second_competitorId = request.data.get('second_competitor')
        date = request.data.get('date')
        hand = request.data.get('hand')
        weight_classId = request.data.get('weight_class')
        category = request.data.get('category')
        round = request.data.get('round')

        if tournamentId is not None and weight_classId is not None and first_competitorId is not None and second_competitorId is not None:
            tournament = Tournament.objects.get(id=tournamentId)
            firstCompetitor = Competitor.objects.get(id=first_competitorId)
            secondCompetitor = Competitor.objects.get(id=second_competitorId)
            weightClass = WeightClass.objects.get(id=weight_classId)
            
            match = Match()
            match.tournament = tournament
            match.first_competitor = firstCompetitor
            match.second_competitor = secondCompetitor
            match.first_competitor_start_rating = firstCompetitor.elo_rating if hand == "left" else firstCompetitor.elo_rating_right
            match.second_competitor_start_rating = secondCompetitor.elo_rating if hand == "left" else secondCompetitor.elo_rating_right
            match.hand = hand
            match.category = category
            match.date = date

            if round is not None:
                match.round = round

            match.weight_class = weightClass
            match.save()
            serializer = MatchSerializer(match)
            return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id is not None:
            try:
                match = Match.objects.get(id=id)
                match.first_competitor.elo_rating = match.first_competitor_start_rating
                match.second_competitor.elo_rating = match.second_competitor_start_rating
                match.first_competitor.save()
                match.second_competitor.save()
                match.delete()
                return Response({"detail": "Match successfully deleted"}, status=status.HTTP_200_OK)
            except Match.DoesNotExist:
                return Response({"detail": "Match not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Id is None"},status=status.HTTP_400_BAD_REQUEST)


class TournamentViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = TournamentSerializer

    @action(detail=False, methods=['post'])
    def start(self, request):
        tournamentId = request.data.get('tournamentId')
        started = request.data.get('started')
        if tournamentId is not None and started is not None:
            tournament = Tournament.objects.get(id=tournamentId)
            tournament.is_started = started
            tournament.save()
            serializer = TournamentSerializer(tournament)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
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
        afisha = request.data.get('afisha',None)

        
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
               
                if afisha is not None:
                    tournament.afisha = afisha
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

class TournamentWeightClassesCreateViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentWeightClassesSerializer
    queryset = TournamentWeightClasses.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()
        tournamentId = self.request.query_params.get('tournamentId',None)
        if tournamentId is not None:
            tournament = Tournament.objects.get(id=tournamentId)
            queryset = TournamentWeightClasses.objects.filter(tournament=tournament)
        return queryset
    
    def create(self, request, *args, **kwargs):
        tournament_id = request.data.get('tournamentId')

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        tournament_weight_classes = []
        for category, weights in request.data.items():
            if category != 'tournamentId':
                for weight_data in weights:
                    weight_name = weight_data['name']
                    
                    try:
                        # Попытка получить существующий объект WeightClass по имени
                        weight_class = WeightClass.objects.get(name=weight_name)
                    except WeightClass.DoesNotExist:
                        # Если объект WeightClass не существует, создаем новый
                        weight_class = WeightClass.objects.create(name=weight_name)

                    # Создание TournamentWeightClass с связанным WeightClass
                    tournament_weight_class = TournamentWeightClasses.objects.create(
                        tournament=tournament,
                        weight_class=weight_class,
                        category=category
                    )
                    
                    tournament_weight_classes.append(tournament_weight_class)

        serializer = TournamentWeightClassesSerializer(tournament_weight_classes, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class TournamentProtocolViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()


    def update(self, request, *args, **kwargs):
        tournament_id = request.data.get('tournamentId',None)
        activated = request.data.get('activated', None)
        mode = request.data.get('mode',None)

        if tournament_id is not None and activated is not None:
            try:
                tournament = Tournament.objects.get(id=tournament_id)
                tournament.is_started = activated
                tournament.mode = mode
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
    queryset = TournamentRegistration.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TournamentRegistrationPOSTSerializer
        return TournamentRegistrationSerializer


    class Meta:
        model = TournamentRegistration
        fields = '__all__'

    def update(self, request, *args, **kwargs):
        id = request.data.get('id')
        weight_class = request.data.get('weight_class')
        category = request.data.get('category')
        confirm = request.data.get('confirm')
        weight = request.data.get('weight')
        paid = request.data.get('paid')
        hand = request.data.get('hand')
        if id is not None:
            registration = TournamentRegistration.objects.get(id=id)
            if weight_class is not None:
                registration.weight_class = WeightClass.objects.get(id=weight_class)
            if category is not None:
                registration.category = category
            if confirm is not None:
                registration.confirm = confirm
            if weight is not None:
                registration.weight = weight
            if paid is not None:
                registration.paid = paid
            if hand is not None:
                registration.hand = hand
            registration.save()
            serializer = TournamentRegistrationSerializer(registration)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def create(self, request, *args, **kwargs):
        tournament = request.data.get('tournament')
        competitor = request.data.get('competitor')
        weight_class = request.data.get('weight_class')
        category = request.data.get('category')
        hand = request.data.get('hand')

        try:
            tournament_obj = Tournament.objects.get(id=tournament)
            competitor_obj = Competitor.objects.get(id=competitor)
            tournament_weight_class_obj = TournamentWeightClasses.objects.get(id=weight_class)
            if tournament_weight_class_obj:
                weight_class_obj = tournament_weight_class_obj.weight_class
        
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except Competitor.DoesNotExist:
            return Response({'error': 'Competitor does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except TournamentWeightClasses.DoesNotExist:
            return Response({'error': 'Weight Class does not exist.'},status=status.HTTP_400_BAD_REQUEST)

        if TournamentRegistration.objects.filter(tournament=tournament_obj, competitor=competitor_obj, weight_class=weight_class_obj,hand=hand).exists():
            return Response({'error': 'Tournament registration already exists.'}, status=status.HTTP_401_UNAUTHORIZED)

        existing_registration = TournamentRegistration.objects.filter(
            tournament=tournament_obj,
            competitor=competitor_obj,
            weight_class=weight_class_obj,
            hand=hand
        )

        if existing_registration.exists():
            return Response({'error': 'Registration already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            registration = TournamentRegistration()
            registration.tournament = tournament_obj
            registration.competitor = competitor_obj
            registration.category = category
            registration.weight_class = weight_class_obj
            if hand is not None:
                registration.hand = hand
            registration.save()
            serializer = TournamentRegistrationSerializer(registration)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = super().get_queryset()
        tournament_id = self.request.query_params.get('tournamentId', None)
        id = self.request.query_params.get('id',None)
        if tournament_id is not None:
            tournament = Tournament.objects.get(id=tournament_id)
            queryset = queryset.filter(tournament=tournament)
        elif id is not None:
            queryset = queryset.filter(id=id)
        else:
            return Response({'error': 'Registered Competitors for this tournament not found.'})
        return queryset


class TournamentRegistrationConfirmViewSet(viewsets.ModelViewSet):
    queryset = TournamentRegistration.objects.all()

    def update(self, request, *args, **kwargs):
        id = request.data.get('id')
        if id is not None:
            exists = TournamentRegistration.objects.filter(id=id)
            if exists.exists():
                registration = TournamentRegistration.objects.get(id=id)
                registration.confirm = True
                registration.save()
                serializer = TournamentRegistrationSerializer(registration)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TournamentRegistrationDeleteViewSet(viewsets.ModelViewSet):
    queryset = TournamentRegistration.objects.all()
    serializer_class =TournamentRegistrationSerializer
    def destroy(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id is not None:
            try:
                registration = TournamentRegistration.objects.get(id=id)
                registration.delete()
                return Response({"detail": "League successfully deleted"}, status=status.HTTP_200_OK)
            except TournamentRegistration.DoesNotExist:
                return Response({"detail": "League not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Id is None"},status=status.HTTP_400_BAD_REQUEST)


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

    def create(self, request, *args, **kwargs):
        competitor = request.data.get('competitor')
        tournament = request.data.get('tournament')
        read  = request.data.get('read')
        datetime = request.data.get('datetime')
        message = request.data.get('message')
        if competitor is not None and tournament is not None:
            competitor_instance = Competitor.objects.get(id=competitor)
            tournament_instance = Tournament.objects.get(id=tournament)

            # Используйте filter вместо get
            exists = TournamentNotification.objects.filter(tournament=tournament_instance)

            if not exists.exists():
                notification = TournamentNotification()
                notification.competitor = competitor_instance
                notification.tournament = tournament_instance
                notification.message = message
                notification.read = read
                notification.datetime = datetime
                notification.save()
                serializer = TournamentNotificationSerializer(notification)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SupportRequestViewSet(viewsets.ModelViewSet):
    serializer_class = SupportRequestSerializer
    queryset = SupportRequest.objects.all()

# PASWORD RESTORE ##################

def send_restore_password_link(user, password):
    subject = 'Восстановление пароля'
    html_message = render_to_string('password_restore_template.html', {'password': password, 'server_url': 'http://127.0.0.1:8000' if settings.DEBUG else 'http://apm-tech.ru'})
    plain_message = strip_tags(html_message)
    from_email = 'Armwrestling.promotion.machine@gmail.com'  # Замените на ваш адрес электронной почты
    to_email = user.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

def generate_password(length=8):
    letters = ''.join(secrets.choice(string.ascii_letters) for _ in range(6))
    digit = secrets.choice(string.digits)
    punctuation = secrets.choice(string.punctuation)
    password = letters + digit + punctuation
    password = ''.join(secrets.choice(password) for _ in range(length))
    return password

class PasswordRestoreViewSet(viewsets.ModelViewSet):
    serializer_class = CompetitorSerializer

    @action(detail=False, methods=['GET'])
    def restore_passord(self, request, pk=None):
        email = request.query_params.get('email')
        if email is not None:
            competitor = Competitor.objects.filter(email=email)
            if competitor.exists():
                try:
                    competitor_obj = Competitor.objects.get(email=email)
                    new_pass = generate_password()
                    competitor_obj.set_password(new_pass)
                    competitor_obj.save()
                    update_session_auth_hash(request, competitor_obj)
                    send_restore_password_link(competitor_obj,new_pass)
                    # Вернуть отрендеренный ответ
                    return Response({'detail': 'Password updated successfully'}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    print(f"Error: {e}")
                    return Response({'detail': 'Error updating password'}, status=status.HTTP_400_BAD_REQUEST)
                

class TeamCompetitorViewSet(viewsets.ModelViewSet):
    queryset = TeamCompetitor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeamCompetitorPOSTSerializer
        return TeamCompetitorSerializer
    
    def create(self, request, *args, **kwargs):
        competitor = request.data.get('competitor')
        team = request.data.get('team')
        status = request.data.get('status')

        if competitor is not None and team is not None and status is not None:
            competitor_obj = Competitor.objects.get(id=competitor)
            team_obj = Team.objects.get(id=team)

            exists = TeamCompetitor.objects.filter(competitor=competitor_obj,team=team_obj)
            if not exists.exists():
                instance = TeamCompetitor()
                instance.competitor =competitor_obj
                instance.team = team_obj
                instance.status = status
                instance.save()
                serializer = TeamCompetitorSerializer(instance)
                return Response(serializer.data)
        else:
           return Response({'detail': 'Data is empty'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        competitorId = self.request.query_params.get('competitorId')
        teamId = self.request.query_params.get('teamId')

        if competitorId is not None:
            competitor = Competitor.objects.get(id=competitorId)
            queryset = queryset.filter(competitor=competitor)
        if teamId is not None:
            team = Team.objects.get(id=teamId)
            queryset = queryset.filter(team=team)
        return queryset


class TeamCompetitorAcceptViewSet(viewsets.ModelViewSet):
    serializer_class = TeamCompetitorPOSTSerializer
    queryset = TeamCompetitor.objects.all()

    def update(self, request, *args, **kwargs):
        competitorId = request.data.get("competitorId")
        status = request.data.get("status")

        if competitorId is not None:
            exists = TeamCompetitor.objects.filter(id=competitorId)
            if exists.exists():
                competitor_team_obj = TeamCompetitor.objects.get(id=competitorId)
                competitor_team_obj.status = status
                competitor_team_obj.save()
                serializer = TeamCompetitorSerializer()
                return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        organizerId = self.request.query_params.get('organizerId')

        if organizerId is not None:
            organizer = Competitor.objects.get(id=organizerId)
            queryset = queryset.filter(organizer=organizer)
        return queryset
    

    def create(self, request, *args, **kwargs):
        organizerId = request.data.get('organizerId')
        name = request.data.get('name')

        if organizerId is not None:   
            organizer = Competitor.objects.filter(id=organizerId)
            if organizer.exists():
                team = Team()
                organizer_instance = Competitor.objects.get(id=organizerId)
                team.organizer = organizer_instance 
                team.name = name
                team.save()
                serializer = TeamSerializer(team)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            

    def update(self, request, *args, **kwargs):
        teamId = request.data.get('teamId')
    
        description = request.data.get('description')
        location = request.data.get('location')
        email = request.data.get('email')
        phone = request.data.get('phone')
        status = request.data.get('status')
        country = request.data.get('country')
        name = request.data.get('name')
    
        if teamId is not None:   
            try:
                team = Team.objects.get(id=teamId)
                team.name = name
                team.country = country
                team.phone = phone
                team.email = email
                team.description = description
                team.location = location
                team.status = status
                team.save()
               
                serializer = TeamSerializer(team)
                return Response(serializer.data)
            except Team.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    
class TournamentParamsViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentParamsSerializer
    queryset = TournamentParams.objects.all()