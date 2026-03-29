from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import ClientForm, VehicleForm
from .models import Client, Vehicle


class ListClientsView(generic.ListView):
    model = Client
    template_name = "clients/clients_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        queryset = Client.objects.all()
        client_is_active = self.request.GET.get("active")

        if client_is_active == "false":
            queryset = queryset.filter(is_active=False)
        else:
            queryset = queryset.filter(is_active=True)

        return queryset


class ListVehiclesView(generic.ListView):
    model = Vehicle
    template_name = "vehicles/vehicles_list.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        return Vehicle.objects.filter(is_active=True, client__is_active=True)


class ClientDetailView(generic.DetailView):
    model = Client
    template_name = "clients/client_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        vehicles = self.object.vehicles.all()  # related_name

        vehicle_is_active = self.request.GET.get("active")

        if vehicle_is_active == "false":
            vehicles = vehicles.filter(is_active=False)
        else:
            vehicles = vehicles.filter(is_active=True)

        context["vehicles"] = vehicles
        return context


class VehicleDetailView(generic.DetailView):
    model = Vehicle
    template_name = "vehicles/vehicle_detail.html"


class CreateClientView(generic.CreateView):
    model = Client
    template_name = "clients/client_create.html"
    form_class = ClientForm
    success_url = reverse_lazy("clients:clients_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente criado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao criar cliente.")
        return super().form_invalid(form)


class CreateVehicleView(generic.CreateView):
    model = Vehicle
    template_name = "vehicles/vehicles_create.html"
    form_class = VehicleForm

    def form_valid(self, form):
        client = get_object_or_404(Client, id=self.kwargs["client_id"])

        form.instance.client = client  # evita double save
        messages.success(self.request, "Veículo criado com sucesso.")

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao criar veículo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "clients:client_detail",
            kwargs={"pk": self.kwargs["client_id"]},
        )


class UpdateClientView(generic.UpdateView):
    model = Client
    template_name = "clients/client_update.html"
    form_class = ClientForm
    success_url = reverse_lazy("clients:clients_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente atualizado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar cliente.")
        return super().form_invalid(form)


class UpdateVehicleView(generic.UpdateView):
    model = Vehicle
    template_name = "vehicles/vehicle_update.html"
    form_class = VehicleForm

    def form_valid(self, form):
        messages.success(self.request, "Veículo atualizado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar veículo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "clients:client_detail",
            kwargs={"pk": self.object.client.id},
        )


class ClientDeleteView(View):
    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)

        client.soft_delete()

        messages.success(
            request,
            f"Cliente {client.name} removido com sucesso.",
        )

        return redirect("clients:clients_list")


class VehicleDeleteView(View):
    def post(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        client_id = vehicle.client.pk

        vehicle.soft_delete()

        messages.success(
            request,
            f"Veículo {vehicle.vehicle_model} removido com sucesso.",
        )

        return redirect("clients:client_detail", pk=client_id)
