from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import datetime

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

class Competitor(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1)
    # weight_class = models.ForeignKey('WeightClass', on_delete=models.CASCADE, related_name='WeightClasses',blank=True)
    elo_rating = models.IntegerField(default=1000)
    country = models.CharField(max_length=50,default="Russia")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    kFactor = models.IntegerField(default=30, blank=True)
    mode = models.CharField(max_length=20,default="competitor", blank=True)
    weight = models.IntegerField(default=0)
    image = models.ImageField(upload_to='media/competitors_userpictures',blank=True)
    rank = models.CharField(default='',blank=True,max_length=12)
    phone = models.CharField(default='',blank=True,max_length=14)
    objects = CompetitorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    def str(self):
        return f"{self.first_name} {self.last_name}"


class League(models.Model):
    name = models.CharField(max_length=100, unique=True,null=False)
    country = models.CharField(max_length=100,null=False)
    description = models.TextField()
    president = models.ForeignKey(Competitor, on_delete=models.CASCADE, default='')
    level = models.CharField(max_length=50,null=False)
    average_rating = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return f'{self.name} , President: {self.president}'

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField()
    league = models.ForeignKey(League, on_delete=models.CASCADE, default='')
    organizer = models.ForeignKey(Competitor, on_delete=models.CASCADE, default='')
    description = models.TextField(default='', blank=True)
    photo = models.ImageField(upload_to='media/tournaments_banners',blank=True)
    avg_rating = models.IntegerField(default='0')
    address = models.CharField(max_length=100,default='')
    is_started = models.BooleanField(default=False)



    main_secretary = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name='tournaments_main_secretary',
        default=''
    )
    main_referee = models.ForeignKey(
        Competitor,
        on_delete=models.CASCADE,
        related_name='tournaments_main_referee',
        default=''
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

    class Meta:
        unique_together = (('competitor', 'tournament'),)
        verbose_name_plural = 'Tournament registrations'

    def __str__(self):
        return f'{self.competitor} - {self.tournament} - {self.registration_date}'


class TournamentWeightClasses(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    weight_class = models.ForeignKey(WeightClass, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)