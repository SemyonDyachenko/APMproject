# Generated by Django 4.1.7 on 2023-10-23 15:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0032_alter_match_created_at_alter_match_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 23, 15, 32, 3, 296659)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 23, 15, 32, 3, 296738)),
        ),
    ]
