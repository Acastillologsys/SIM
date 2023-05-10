from django.urls import path

from . import views

urlpatterns = [
    path(
        route='view_grand_tournament/<int:pk>',
        view=views.view_grand_tournament,
        name='view_grand_tournament'
    ),
]