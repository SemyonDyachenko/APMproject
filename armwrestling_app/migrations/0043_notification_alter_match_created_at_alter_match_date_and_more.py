# Generated by Django 4.1.7 on 2023-11-11 17:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0042_tournament_active_alter_match_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('datetime', models.DateTimeField()),
                ('read', models.BooleanField(default=False)),
                ('competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 11, 20, 5, 1, 121423)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 11, 20, 5, 1, 121423)),
        ),
        migrations.CreateModel(
            name='TournamentNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='armwrestling_app.notification')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='armwrestling_app.tournament')),
            ],
            bases=('armwrestling_app.notification',),
        ),
    ]