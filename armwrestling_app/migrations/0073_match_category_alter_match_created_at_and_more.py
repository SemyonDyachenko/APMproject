# Generated by Django 4.1.7 on 2024-03-09 10:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0072_alter_match_created_at_alter_match_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='category',
            field=models.CharField(default='men', max_length=50),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 9, 13, 34, 26, 536997)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 9, 13, 34, 26, 536997)),
        ),
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 9, 13, 34, 26, 532987)),
        ),
        migrations.AlterField(
            model_name='teamcompetitor',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 9, 13, 34, 26, 535997)),
        ),
    ]