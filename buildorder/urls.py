from django.urls import path

from . import views

urlpatterns = [
    path(
        route='new_building_order',
        view=views.new_building_order,
        name='new_building_order'
    ),
    path(
        route='BuildOrders',
        view=views.BuildOrders.as_view(),
        name='BuildOrders'
    ),
    path(
        route='view_build_order/<int:pk>',
        view=views.view_build_order,
        name='view_build_order'
    ),
]