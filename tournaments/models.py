from django.db import models
from team.models import Tournament
# Create your models here.


class GrandTournament(models.Model):
    """Grandes Torneos"""
    name = models.CharField(max_length=140)
    description = models.TextField(default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name


class TournamentAgroup(models.Model):
    """Une los grandes torneos con torneos pequeños"""
    grand_tournament = models.ForeignKey(GrandTournament, on_delete=models.DO_NOTHING)
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.grand_tournament.name