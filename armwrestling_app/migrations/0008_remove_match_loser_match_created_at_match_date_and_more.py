# Generated by Django 4.1.7 on 2023-03-26 13:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0007_remove_tournament_weight_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='loser',
        ),
        migrations.AddField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 26, 13, 46, 29, 936626)),
        ),
        migrations.AddField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 26, 13, 46, 29, 936704)),
        ),
        migrations.AddField(
            model_name='match',
            name='hand',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
