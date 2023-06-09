from django.db import models

# Create your models here.


class TournamentStatus(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name


class Tournament(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(default='Torneo Sacro Imperio Manco')
    points_wins = models.IntegerField(default=1)
    status = models.ForeignKey(TournamentStatus, on_delete=models.DO_NOTHING)
    number_teams = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name


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

    def __str__(self):
        return '%s' % self.name


class TournamentJourney(models.Model):
    journey = models.IntegerField(default=0)
    local_gamer = models.CharField(max_length=140, default='')
    visitor_gamer = models.CharField(max_length=140, default='')
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    wins_local_gamer = models.IntegerField(default=0)
    wins_visitor_gamer = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s - %s' % (self.tournament.name, self.local_gamer, self.visitor_gamer)


class Stream(models.Model):
    """streams"""
    tournament_journey = models.ForeignKey(TournamentJourney, on_delete=models.DO_NOTHING)
    link = models.TextField(default='')
    description = models.TextField(default='')
    streamer = models.CharField(max_length=250, default='Desconocido')
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s - %s' % (self.tournament_journey.tournament.name, self.tournament_journey.local_gamer  ,self.tournament_journey.visitor_gamer )