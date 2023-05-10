from django.shortcuts import render
from .models import *
from team.models import *
from team.views import tabla_general
# Create your views here.


def view_grand_tournament(request, pk):
    """ver los torneos"""
    context = dict()
    torneos_activos = list(TournamentAgroup.objects.values('tournament', 'tournament__name').filter(active=1,
                                                                                  tournament__status=2,
                                                                                  tournament__active=1,
                                                                                  grand_tournament=pk).order_by("tournament__name"))
    grand_tournament = list(GrandTournament.objects.values('name', 'description').filter(id=pk))

    context['grand_tournament'] = grand_tournament[0]

    list_tournaments_total = list()
    for data in torneos_activos:
        dict_tournaments_total = dict()
        total_jugadores = len(TournamentGamer.objects.filter(tournament=data['tournament'], active=1))
        is_teams_list = total_jugadores

        flag_journey = 0
        list_jornadas = list()
        while flag_journey < is_teams_list:
            flag_journey += 1
            jornadas = list(TournamentJourney.objects.values().filter(tournament=data['tournament'], journey=flag_journey))
            if len(jornadas) > 0:
                list_jornadas.append(jornadas)
        tabla_general_data = tabla_general(data['tournament'])

        dict_tournaments_total['tournament'] = data['tournament__name']
        dict_tournaments_total['tabla_general'] = tabla_general_data
        dict_tournaments_total['jornadas'] = list_jornadas

        list_tournaments_total.append(dict_tournaments_total)
    context['list_tournaments_total'] = list_tournaments_total

    return render(request, 'grand_tournament.html', context)