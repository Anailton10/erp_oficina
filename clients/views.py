from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import ClientForm, VehicleForm
from .models import Client, Vehicle


class ListClientsView(generic.ListView):
    model = Client
    template_name = 'clients/list_clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        # pegando todos os clientes
        queryset = Client.objects.all()
        
        # lendo parametro de filtro da URL "active"
        client_is_active = self.request.GET.get('active')

        # Filtando os clientes inativos
        if client_is_active == 'false':
            queryset = queryset.filter(is_active=False)
        
        # Retornando os clientes ativos
        else:
            queryset = queryset.filter(is_active=True)
        
        return queryset


class ListVehiclesView(generic.ListView):
    model = Vehicle
    template_name = 'vehicles/list_vehicles.html'
    context_object_name = 'vehicles'

    def get_queryset(self):
        # Filtrando os veículos pelo status do cliente
        # Retorna apenas os veículos cujo cliente está ativo
        return Vehicle.objects.filter(is_active=True, client__is_active=True)
        
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


class ClientDeleteView(View):
    # Recebe(request) o ID(PK) do cliente vindo da URL 
    def post(self, request, pk):
        # Busca o cliente pelo ID(PK) ou retorna 404 se não encontrado
        client = get_object_or_404(Client, pk=pk)
        # Chama o método de exclusão lógica do cliente, que também desativa os veículos associados
        client.soft_delete()

        messages.success(request, f"Cliente {client.name} removido com sucesso.")
        # Redireciona para a lista de clientes após a exclusão
        return redirect('clients:list_clients')