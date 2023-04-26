from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
# Create your views here.
from .models import *


def new_building_order(request):
    """Crea un nuevo orden"""
    context = dict()
    if request.method == "POST":
        name = request.POST['nombre']
        description = request.POST['descripcion']
        velocidad_juego = request.POST['velocidad']
        aldeanos_iniciales = request.POST['aldeanos_iniciales']
        aldeanos_feudal = request.POST['aldeanos_feudal']
        aldeanos_castillos = request.POST['aldeanos_castillos']
        aldeanos_imperial = request.POST['aldeanos_imperial']

        build_order_create = BuildOrder.objects.create(name=name,
                                                       description=description,
                                                       velocidad_juego=velocidad_juego,
                                                       aldeanos_iniciales=aldeanos_iniciales,
                                                       aldeanos_feudal=aldeanos_feudal,
                                                       aldeanos_castillos=aldeanos_castillos,
                                                       aldeanos_imperial=aldeanos_imperial,
                                                       )

        for act in range(int(request.POST['num_activities'])):
            num_activity = str(act + 1)
            activity = request.POST['activity_name_' + num_activity]
            aldeanos_actividad_anterior = request.POST['activity_hours_' + num_activity]
            BuildOrderPass.objects.create(activity=activity,
                                          build_order=build_order_create,
                                          aldeanos_actividad_anterior=aldeanos_actividad_anterior)
        reverse_url = "../BuildOrders/"
        return HttpResponseRedirect(reverse('buildorder:BuildOrders'))
    else:
        pass

        return render(request, 'create_build_order.html', context)


class BuildOrders(TemplateView):
    """Obtener buildorders"""
    template_name = "build_orders.html"

    def get_context_data(self, **kwargs):
        """obtiene el contexto"""
        args = dict()
        info_build_order = BuildOrder.objects.values('name', 'description', 'id').filter(active=1)
        args['builds_info'] = info_build_order
        return args


def view_build_order(request, pk):
    """ver el build order seleccionado"""
    context = dict()
    build_order_activity = list(BuildOrderPass.objects.values(
                                                     'activity',
                                                     'aldeanos_actividad_anterior'
                                                     ).filter(build_order=pk).order_by("id"))
    list_build_order = list()
    for data in build_order_activity:
        list_build_order.append(data['activity'].replace(",", " "))
        list_build_order.append(data['aldeanos_actividad_anterior'])
    start_list = list()
    start_list.append('Inicio Crear Aldeano 4')
    start_list.append(0)
    build_order_data = list(BuildOrder.objects.values('name',
                                                     'description',
                                                     'velocidad_juego',
                                                     'aldeanos_iniciales',
                                                     'aldeanos_feudal',
                                                     'aldeanos_castillos',
                                                     'aldeanos_imperial',
                                                     ))
    context['build_order'] = build_order_data[0]
    context['build_order_activity'] = start_list + list_build_order
    return render(request, 'view_build_order.html', context)