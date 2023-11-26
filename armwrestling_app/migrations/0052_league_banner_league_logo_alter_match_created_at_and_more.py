# Generated by Django 4.1.7 on 2023-11-26 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0051_competitor_token_alter_match_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='banner',
            field=models.ImageField(blank=True, upload_to='media/league_banner'),
        ),
        migrations.AddField(
            model_name='league',
            name='logo',
            field=models.ImageField(blank=True, upload_to='media/league_logo'),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 26, 18, 28, 19, 88772)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 26, 18, 28, 19, 88772)),
        ),
    ]
