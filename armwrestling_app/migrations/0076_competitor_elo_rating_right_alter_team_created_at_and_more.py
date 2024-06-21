# Generated by Django 4.1.7 on 2024-04-07 12:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0075_tournament_mode_alter_match_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='elo_rating_right',
            field=models.IntegerField(blank=True, default=1000),
        ),
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 7, 15, 57, 57, 987416)),
        ),
        migrations.AlterField(
            model_name='teamcompetitor',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 7, 15, 57, 57, 989414)),
        ),
    ]