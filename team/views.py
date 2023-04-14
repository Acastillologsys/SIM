from django.shortcuts import render
import itertools
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, views as auth_views

def emparejar_jugadores(jugadores):
    n = len(jugadores)
    if n % 2 != 0:
        # Si el número de jugadores es impar, agregamos un falso jugador llamado BYE
        jugadores.append('Descanso')
        n += 1

    mitad = n // 2
    jornadas = []
    for i in range(n - 1):
        # Generamos las parejas de jugadores para cada jornada
        parejas = list(zip(jugadores[:mitad], reversed(jugadores[mitad:])))
        jornadas.append(parejas)
        jugadores.insert(1, jugadores.pop())

    return jornadas


def resultados(request):
    jugadores = ['Jugador 1', 'Jugador 2', 'Jugador 3', 'Jugador 4', 'jugador 5', 'jugador 6', 'jugador 7']
    numero_jugadores = len(jugadores)
    # Generamos los resultados de los emparejamientos
    jornadas = emparejar_jugadores(jugadores)
    # Dividimos los resultados en jornadas

    return render(request, 'resultados.html', {'jornadas': jornadas})

@login_required
def create_torunament(request):
    if request.method == "POST":
        name = request.POST.get('torneo', False)
        description = request.POST.get('descripcion_torneo', False)
        points_wins = request.POST.get('points_wins', False)
        number_teams = request.POST.get('number_teams', False)
        status = TournamentStatus.objects.get(id=1)
        tournament = Tournament.objects.create(name=name, description=description, status=status,
                                               points_wins=points_wins, number_teams=number_teams)
        reverse_url = "team/view_tournament"
        return HttpResponseRedirect(reverse_url)
    else:
        return render(request, 'create_torunament.html')


def view_tournament(request):
    """ver los torneos"""
    context = dict()
    context['tournament_open'] = Tournament.objects.values().filter(status=1)
    context['tournament_started'] = Tournament.objects.values().filter(status=2)
    context['tournament_finished'] = Tournament.objects.values().filter(status=3)

    return render(request, 'view_tournament.html', context)


def join_tournament(request, pk):
    context = dict()
    if request.method == "POST":
        name = request.POST.get('username', False)
        elo = request.POST.get('elo', False)

        gamer_1 = request.POST.get('gamer_1', False)
        gamer_1_elo = request.POST.get('gamer_1_elo', False)
        gamer_2 = request.POST.get('gamer_2', False)
        gamer_2_elo = request.POST.get('gamer_2_elo', False)
        gamer_3 = request.POST.get('gamer_3', False)
        gamer_3_elo = request.POST.get('gamer_3_elo', False)
        gamer_4 = request.POST.get('gamer_4', False)
        gamer_4_elo = request.POST.get('gamer_4_elo', False)

        tournament = Tournament.objects.get(id=pk)
        TournamentGamer.objects.create(name=name, elo=elo, tournament=tournament, gamer_1=gamer_1,
                                       gamer_1_elo=gamer_1_elo, gamer_2=gamer_2, gamer_2_elo=gamer_2_elo,
                                       gamer_3=gamer_3, gamer_3_elo=gamer_3_elo, gamer_4=gamer_4,
                                       gamer_4_elo=gamer_4_elo)
        reverse_url = "../team/view_tournament"
        return HttpResponseRedirect(reverse_url)
    else:
        tournament_gamers = TournamentGamer.objects.values().filter(tournament=pk)
        tournament_data = Tournament.objects.values().filter(id=pk)[:1]
        context['tournament'] = tournament_data[0]
        is_teams_list = list(range(tournament_data[0]['number_teams'] + 1))
        is_teams_list.pop(0)
        context['is_teams'] = is_teams_list
        context['tournament_gamers'] = tournament_gamers
        context['gamers_joined'] = len(tournament_gamers)
        context['id_tournament'] = pk
        return render(request, 'join_tournament.html', context)


def create_tournament_journey(request, pk):
    tournament_gamers = list(TournamentGamer.objects.values_list('name', flat=True).filter(tournament=pk))

    jornadas = emparejar_jugadores(tournament_gamers)
    # Dividimos los resultados en jornadas
    journey_number = 0
    tournament = Tournament.objects.get(id=pk)
    for jornada in jornadas:
        journey_number += 1
        for local, visitante in jornada:
            TournamentJourney.objects.create(journey=journey_number, local_gamer=local, visitor_gamer=visitante,
                                             tournament=tournament)
    status = TournamentStatus.objects.get(id=2)
    Tournament.objects.values(id=pk).update(status=status)
    reverse_url = "../team/view_tournament_journey/" + str(pk)
    return HttpResponseRedirect(reverse_url)


def view_tournament_journey(request, pk):
    context = dict()
    if request.method == "POST":
        jornada = request.POST.get('jornada', False)
        local_gamer_marcador = request.POST.get('local_gamer_marcador', False)
        visitor_gamer_marcador = request.POST.get('visitor_gamer_marcador', False)
        TournamentJourney.objects.filter(tournament=pk,
                                         id=jornada).update(wins_local_gamer=local_gamer_marcador,
                                                                 wins_visitor_gamer=visitor_gamer_marcador)
        total_jugadores = len(TournamentGamer.objects.filter(tournament=pk, active=1))
        is_teams_list = total_jugadores

        flag_journey = 0
        list_jornadas = list()
        while flag_journey < is_teams_list:
            flag_journey += 1
            jornadas = list(TournamentJourney.objects.values().filter(tournament=pk, journey=flag_journey))
            list_jornadas.append(jornadas)
        tabla_general_data = tabla_general(pk)
        context['tabla_general'] = tabla_general_data
        context['jornadas'] = list_jornadas
        return render(request, 'view_tournament_journey.html', context)
    else:
        total_jugadores = len(TournamentGamer.objects.filter(tournament=pk, active=1))
        is_teams_list = total_jugadores

        flag_journey = 0
        list_jornadas = list()
        while flag_journey < is_teams_list:
            flag_journey += 1
            jornadas = list(TournamentJourney.objects.values().filter(tournament=pk, journey=flag_journey))
            list_jornadas.append(jornadas)
        tabla_general_data = tabla_general(pk)
        context['tabla_general'] = tabla_general_data
        context['jornadas'] = list_jornadas
        return render(request, 'view_tournament_journey.html', context)


def inicio_session(request):
    """Login view."""
    args = dict()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            reverse_url = "team/view_tournament"
            return HttpResponseRedirect(reverse_url)
        else:
            return render(request, 'login.html', args)
    else:
        return render(request, 'login.html', args)


class LogoutView(auth_views.LogoutView):
    """Logout view."""

    template_name = 'login.html'


def tabla_general(id):
    data_gamers = TournamentGamer.objects.values('name', 'elo').filter(tournament=id)
    list_gamer = list()
    for data in data_gamers:
        dic_gamer = dict()
        points_local = TournamentJourney.objects.values('local_gamer', 'wins_local_gamer').filter(local_gamer=data['name'], tournament=id)
        points_visit = TournamentJourney.objects.values('visitor_gamer', 'wins_visitor_gamer').filter(visitor_gamer=data['name'], tournament=id)
        puntos_local_suma = 0
        for data_local in points_local:
            puntos_local_suma += data_local['wins_local_gamer']

        puntos_visitante_suma = 0
        for data_visitante in points_visit:
            puntos_visitante_suma += data_visitante['wins_visitor_gamer']

        puntos_totales = puntos_local_suma + puntos_visitante_suma
        dic_gamer['gamer'] = data['name']
        dic_gamer['points'] = puntos_totales
        dic_gamer['id'] = str(puntos_totales) + '_' + data['name']
        list_gamer.append(dic_gamer)
    list_gamer = sorted(list_gamer, key=lambda k: k['id'], reverse=True)
    lugar = 1
    for data in list_gamer:
        data['lugar'] = lugar
        lugar +=1
    return list_gamer