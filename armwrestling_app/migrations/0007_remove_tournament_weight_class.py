# Generated by Django 4.1.7 on 2023-03-24 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('armwrestling_app', '0006_alter_tournament_weight_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='weight_class',
        ),
    ]