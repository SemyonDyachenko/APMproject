# Generated by Django 4.1.7 on 2024-04-16 11:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0076_competitor_elo_rating_right_alter_team_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='round',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 16, 14, 31, 35, 108589)),
        ),
        migrations.AlterField(
            model_name='teamcompetitor',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 16, 14, 31, 35, 111589)),
        ),
    ]