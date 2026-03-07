from django.views import generic

from .models import Client, Vehicle


class ListClientsView(generic.ListView):
    model = Client
    template_name = 'clients/list_clients.html'
    context_object_name = 'clients'


class ListVehiclesView(generic.ListView):
    model = Vehicle
    template_name = 'vehicles/list_vehicles.html'
    context_object_name = 'vehicles'


class ClientDetailView(generic.DetailView):
    model = Client
    template_name = 'clients/client_detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['vehicles'] = self.object.vehicles.all()
        return context

class VehicleDetailView(generic.DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'