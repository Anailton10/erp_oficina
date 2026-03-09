from django.urls import reverse_lazy
from django.views import generic

from .forms import ClientForm, VehicleForm
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
    template_name = 'clients/detail_clients.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['vehicles'] = self.object.vehicles.all()
        return context

class VehicleDetailView(generic.DetailView):
    model = Vehicle
    template_name = 'vehicles/detail_vehicles.html'

class CreateClientView(generic.CreateView):
    model = Client
    template_name = 'clients/create_clients.html'
    form_class = ClientForm
    success_url = reverse_lazy('clients:list_clients')


class CreateVehicleView(generic.CreateView):
    model = Vehicle
    template_name = 'vehicles/create_vehicles.html'
    form_class = VehicleForm

    def form_valid(self, form):
        client_id = self.kwargs['client_id']
        client = Client.objects.get(id=client_id)

        vehicle = form.save(commit=False)
        vehicle.client = client
        vehicle.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        client_id = self.kwargs['client_id']
        return reverse_lazy('clients:client_detail', kwargs={'pk': client_id})
    