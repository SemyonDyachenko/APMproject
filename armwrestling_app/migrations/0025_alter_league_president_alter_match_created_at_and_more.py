# Generated by Django 4.1.7 on 2023-10-15 19:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0024_competitor_image_alter_match_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='president',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 15, 22, 2, 59, 357574)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 15, 22, 2, 59, 357574)),
        ),
    ]
