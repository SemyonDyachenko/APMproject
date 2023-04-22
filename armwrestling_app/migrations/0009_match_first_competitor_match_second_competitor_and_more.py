# Generated by Django 4.1.7 on 2023-03-26 13:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0008_remove_match_loser_match_created_at_match_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='first_competitor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='firstcompetitor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='match',
            name='second_competitor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='secondcompetitor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 26, 13, 53, 24, 711509)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 26, 13, 53, 24, 711568)),
        ),
    ]
