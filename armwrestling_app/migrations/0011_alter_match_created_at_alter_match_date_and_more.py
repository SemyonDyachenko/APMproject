# Generated by Django 4.1.7 on 2023-03-26 14:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0010_alter_match_created_at_alter_match_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 26, 14, 1, 18, 741975)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 26, 14, 1, 18, 742015)),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wins', to=settings.AUTH_USER_MODEL),
        ),
    ]