from django.urls import path

from . import views

urlpatterns = [
    path(
        route='create_torunament',
        view=views.create_torunament,
        name='create_torunament'
    ),
    path(
        route='view_tournament',
        view=views.view_tournament,
        name='view_tournament'
    ),
    path(
        route='join_tournament/<int:pk>',
        view=views.join_tournament,
        name='join_tournament'
    ),
    path(
        route='create_tournament_journey/<int:pk>',
        view=views.create_tournament_journey,
        name='create_tournament_journey'
    ),
    path(
        route='view_tournament_journey/<int:pk>',
        view=views.view_tournament_journey,
        name='view_tournament_journey'
    ),
    path(
        route='',
        view=views.inicio_session,
        name='tam_inicio_session'
    ),
    path(
        route='inicio_session',
        view=views.inicio_session,
        name='inicio_session'
    ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
]