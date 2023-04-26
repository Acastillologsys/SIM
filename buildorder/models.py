from django.db import models

# Create your models here.


class BuildOrder(models.Model):
    name = models.CharField(max_length=140, default='')
    description = models.TextField(default='')
    velocidad_juego = models.FloatField(default=1.7)
    aldeanos_iniciales = models.IntegerField()
    aldeanos_feudal = models.IntegerField(default=29)
    aldeanos_castillos = models.IntegerField(default=31)
    aldeanos_imperial = models.IntegerField(default=35)
    active = models.BooleanField(default=True)


class BuildOrderPass(models.Model):
    """Pasos a seguir"""
    build_order = models.ForeignKey(BuildOrder, on_delete=models.DO_NOTHING)
    order = models.IntegerField(default=0)
    activity = models.CharField(max_length=500, default='')
    aldeanos_actividad_anterior = models.IntegerField(default=15)
    active = models.BooleanField(default=True)