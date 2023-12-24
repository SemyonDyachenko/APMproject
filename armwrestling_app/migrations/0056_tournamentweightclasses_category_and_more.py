# Generated by Django 4.1.7 on 2023-11-28 13:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0055_tournament_afisha_alter_match_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentweightclasses',
            name='category',
            field=models.CharField(blank=True, default='men', max_length=50),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 28, 16, 32, 30, 173700)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 28, 16, 32, 30, 173700)),
        ),
    ]