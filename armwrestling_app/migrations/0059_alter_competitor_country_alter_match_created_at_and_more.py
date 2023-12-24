# Generated by Django 4.1.7 on 2023-12-11 07:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0058_supportrequest_alter_match_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='country',
            field=models.CharField(default='Россия', max_length=50),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 11, 10, 29, 3, 777113)),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 11, 10, 29, 3, 777113)),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 12, 11, 10, 29, 3, 782113))),
                ('status', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]