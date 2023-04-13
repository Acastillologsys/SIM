from django.db import models

# Create your models here.


class TournamentStatus(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(default='')
    active = models.BooleanField(default=True)


class Tournament(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(default='Torneo Sacro Imperio Manco')
    points_wins = models.IntegerField(default=1)
    status = models.ForeignKey(TournamentStatus, on_delete=models.DO_NOTHING)
    number_teams = models.IntegerField(default=0)
    active = models.BooleanField(default=True)


class TournamentGamer(models.Model):
    name = models.CharField(max_length=140)
    elo = models.IntegerField(default=1000)
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    gamer_1 = models.CharField(max_length=140, default='')
    gamer_1_elo = models.IntegerField(default=1000)
    gamer_2 = models.CharField(max_length=140, default='')
    gamer_2_elo = models.IntegerField(default=1000)
    gamer_3 = models.CharField(max_length=140, default='')
    gamer_3_elo = models.IntegerField(default=1000)
    gamer_4 = models.CharField(max_length=140, default='')
    gamer_4_elo = models.IntegerField(default=1000)
    active = models.BooleanField(default=True)


class TournamentJourney(models.Model):
    journey = models.IntegerField(default=0)
    local_gamer = models.CharField(max_length=140, default='')
    visitor_gamer = models.CharField(max_length=140, default='')
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    wins_local_gamer = models.IntegerField(default=0)
    wins_visitor_gamer = models.IntegerField(default=0)
    active = models.BooleanField(default=True)