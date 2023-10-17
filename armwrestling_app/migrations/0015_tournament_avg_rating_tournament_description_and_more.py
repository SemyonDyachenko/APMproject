# Generated by Django 4.1.7 on 2023-04-06 11:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0014_competitor_kfactor_competitor_mode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='avg_rating',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='tournament',
            name='main_referee',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='tournaments_main_referee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tournament',
            name='main_secretary',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='tournaments_main_secretary', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tournament',
            name='organizer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tournament',
            name='photo',
            field=models.ImageField(default=2, upload_to='tournaments_banners'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 11, 26, 2, 956016)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 11, 26, 2, 956047)),
        ),
    ]