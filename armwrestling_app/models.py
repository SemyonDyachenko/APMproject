from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.mail import message,send_mail
import uuid

class WeightClass(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CompetitorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Team(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    status = models.CharField(max_length=30,blank=True)
    organizer = models.ForeignKey('Competitor',on_delete=models.CASCADE,related_name='team_organizer')
    phone = models.CharField(max_length=30,blank=True)
    email = models.EmailField(max_length=100,blank=True)
    country = models.CharField(max_length=100,blank=True)
    location = models.CharField(max_length=100,blank=True)

    logo = models.ImageField(upload_to='media/teams_logo',blank=True)
    banner = models.ImageField(upload_to='media/teams_banner',blank=True)



class Competitor(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1)
    # weight_class = models.ForeignKey('WeightClass', on_delete=models.CASCADE, related_name='WeightClasses',blank=True)
    elo_rating = models.IntegerField(default=1000)
    country = models.CharField(max_length=50,default="Россия")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    kFactor = models.IntegerField(default=30, blank=True)
    mode = models.CharField(max_length=20,default="competitor", blank=True)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    trainer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(default='',blank=True,max_length=50)
    description = models.TextField(default=0,blank=True)
    career_start_date = models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to='media/competitors_userpictures',blank=True)
    rank = models.CharField(default='',blank=True,max_length=12)
    phone = models.CharField(default='',blank=True,max_length=17)
    birthdate = models.DateField(null=True,blank=True)
    verified = models.BooleanField(default=False,blank=True)
    
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='competitor_team',null=True,blank=True)
    
    objects = CompetitorManager()

    # stats
    grip = models.IntegerField(blank=True,default=0)
    biceps = models.IntegerField(blank=True,default=0)
    crossbar = models.IntegerField(blank=True,default=0)
    shaft = models.IntegerField(blank=True,default=0)
    militarypress = models.IntegerField(blank=True,default=0)
    hand = models.IntegerField(blank=True,default=0)
    press = models.IntegerField(blank=True,default=0)
    side = models.IntegerField(blank=True,default=0)

    token = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    def str(self):
        return f"{self.first_name} {self.last_name}"


class TeamCompetitor(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    competitor = models.ForeignKey(Competitor,on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.datetime.now())
    status = models.CharField(max_length=30)



class League(models.Model):
    name = models.CharField(max_length=100, unique=True,null=False)
    country = models.CharField(max_length=100,null=False)
    description = models.TextField()
    president = models.ForeignKey(Competitor, on_delete=models.CASCADE, default='')
    level = models.CharField(max_length=50,null=False)
    average_rating = models.IntegerField(blank=True,default=0)
    creation_date = models.DateField(blank=True,null=True)
    phone=models.CharField(blank=True,default='',max_length=15)
    email = models.CharField(blank=True,default='',max_length=99)


    logo = models.ImageField(upload_to='media/league_logo',blank=True)
    banner = models.ImageField(upload_to='media/league_banner',blank=True)

    def __str__(self):
        return f'{self.name} , President: {self.president}'

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField()
    league = models.ForeignKey(League, on_delete=models.CASCADE, default='',blank=True)
    organizer = models.ForeignKey(Competitor, on_delete=models.CASCADE, default='')
    description = models.TextField(default='', blank=True)
    banner = models.ImageField(upload_to='media/tournaments_banners',blank=True)
    avg_rating = models.IntegerField(default='0')
    address = models.CharField(max_length=100,default='')
    is_started = models.BooleanField(default=False)
    phone = models.CharField(blank=True,default="",max_length=25)
    level = models.CharField(blank=True,default="",max_length=15)
    active = models.BooleanField(blank=True,default=False)

    afisha = models.ImageField(upload_to='media/tournaments_afisha',blank=True)
    logo = models.ImageField(upload_to='media/tournaments_logo',blank=True)

    main_secretary = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name='tournaments_main_secretary',
        default='',
        blank=True,
        null=True
    )
    main_referee = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name='tournaments_main_referee',
        default='',
        blank=True,
        null=True
    )

    


    def __str__(self):
        return f"{self.name}"


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    weight_class = models.ForeignKey(WeightClass, on_delete=models.CASCADE)
    winner = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='wins', null=True,blank=True)
    first_competitor = models.ForeignKey(Competitor,default=None, on_delete=models.CASCADE,related_name='firstcompetitor')
    second_competitor = models.ForeignKey(Competitor,default=None,on_delete=models.CASCADE,related_name='secondcompetitor')

    created_at = models.DateTimeField(default=datetime.datetime.now())
    date = models.DateTimeField(default=datetime.datetime.now())
    hand = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.first_competitor} vs. {self.second_competitor}'


class TournamentRegistration(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    weight_class = models.ForeignKey(WeightClass, on_delete=models.CASCADE,default='')
    registration_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50,blank=True,default="")
    confirm = models.BooleanField(default=False,blank=True)
    weight = models.FloatField(blank=True,default=0.0)
    paid = models.BooleanField(blank=True,default=False)
    hand = models.CharField(blank=True,default='left',max_length=20)

    class Meta:
        verbose_name_plural = 'Tournament registrations'

    def __str__(self):
        return f'{self.competitor} - {self.tournament} - {self.registration_date}'




class TournamentWeightClasses(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    weight_class = models.ForeignKey(WeightClass, on_delete=models.CASCADE)
    category = models.CharField(max_length=50,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    rating = models.FloatField(default=None,blank=True)
    text = models.TextField()
    author = models.ForeignKey(Competitor,on_delete=models.CASCADE)
    date = models.DateField(default=None,blank=True)
    verified = models.BooleanField(default=False,blank=True)


class TournamentReview(Review):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE)

class LeagueReview(Review):
    league = models.ForeignKey(League,on_delete=models.CASCADE)


class Notification(models.Model):
    competitor = models.ForeignKey(Competitor,on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    datetime = models.DateTimeField()
    read = models.BooleanField(blank=False,default=False)


class TournamentNotification(Notification):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE)


class LeagueCompetitor(models.Model):
    league = models.ForeignKey(League,on_delete=models.CASCADE)
    competitor = models.ForeignKey(Competitor,on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    status = models.CharField(default='sent',max_length=20)
    request_date = models.DateField(blank=True,default='')
    role = models.CharField(max_length=35,default="competitor")
    message = models.TextField(blank=True)

class SupportRequest(models.Model):
    message = models.TextField()
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField(blank=True)
