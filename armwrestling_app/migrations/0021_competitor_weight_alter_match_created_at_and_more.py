# Generated by Django 4.1.7 on 2023-04-08 16:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0020_remove_weightclass_lower_weight_limit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 8, 16, 40, 9, 476178)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 8, 16, 40, 9, 476210)),
        ),
    ]
