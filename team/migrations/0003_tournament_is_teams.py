# Generated by Django 4.2 on 2023-04-13 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_tournamentgamer_gamer_1_tournamentgamer_gamer_1_elo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_teams',
            field=models.BooleanField(default=False),
        ),
    ]
