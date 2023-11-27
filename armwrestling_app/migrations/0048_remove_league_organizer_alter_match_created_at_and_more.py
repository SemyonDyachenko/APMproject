# Generated by Django 4.1.7 on 2023-11-25 19:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0046_remove_tournament_biceps_remove_tournament_crossbar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 22, 13, 58, 809908)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 22, 13, 58, 809908)),
        ),
        migrations.CreateModel(
            name='LeagueCompetitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('request_date', models.DateField(blank=True, default='')),
                ('competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='armwrestling_app.league')),
            ],
        ),
    ]