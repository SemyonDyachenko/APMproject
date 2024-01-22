# Generated by Django 4.1.7 on 2024-01-14 14:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0067_leaguecompetitor_message_alter_match_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentregistration',
            name='confirm',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 14, 17, 8, 55, 320640)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 14, 17, 8, 55, 320640)),
        ),
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 14, 17, 8, 55, 305619)),
        ),
        migrations.AlterField(
            model_name='teamcompetitor',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 14, 17, 8, 55, 320640)),
        ),
    ]
