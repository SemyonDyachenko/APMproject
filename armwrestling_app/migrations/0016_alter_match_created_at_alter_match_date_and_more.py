# Generated by Django 4.1.7 on 2023-04-06 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0015_tournament_avg_rating_tournament_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 11, 26, 20, 392298)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 11, 26, 20, 392336)),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='photo',
            field=models.ImageField(blank=True, upload_to='tournaments_banners'),
        ),
    ]