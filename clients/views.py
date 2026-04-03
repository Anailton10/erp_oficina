from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import ClientForm, VehicleForm
from .models import Client, Vehicle


class ListClientsView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Client
    template_name = "clients/clients_list.html"
    paginate_by = 10
    context_object_name = "clients"
    permission_required = "clients.view_client"

    def get_queryset(self):
        queryset = super().get_queryset()
        client_is_active = self.request.GET.get("active")
        client_name = self.request.GET.get("client_name")

        if client_is_active == "false":
            queryset = queryset.filter(is_active=False)
        else:
            queryset = queryset.filter(is_active=True)

        if client_name:
            queryset = queryset.filter(name__icontains=client_name)
        return queryset


class ListVehiclesView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Vehicle
    template_name = "vehicles/vehicles_list.html"
    context_object_name = "vehicles"
    permission_required = "clients.view_vehicle"

    def get_queryset(self):
        return Vehicle.objects.filter(is_active=True, client__is_active=True)


class ClientDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DetailView,
):
    model = Client
    template_name = "clients/client_detail.html"
    permission_required = "clients.view_client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        vehicles = self.object.vehicles.all()  # type: ignore related_name

        vehicle_is_active = self.request.GET.get("active")

        if vehicle_is_active == "false":
            vehicles = vehicles.filter(is_active=False)
        else:
            vehicles = vehicles.filter(is_active=True)

        context["vehicles"] = vehicles
        return context


class VehicleDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DetailView,
):
    model = Vehicle
    template_name = "vehicles/vehicle_detail.html"
    permission_required = "clients.view_vehicle"


class CreateClientView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView,
):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    permission_required = "clients.add_client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Novo Cliente",
                "button_text": "Salvar",
                "cancel_url": reverse_lazy("clients:clients_list"),
            }
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Cliente criado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao criar cliente.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("clients:clients_list")


class CreateVehicleView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView,
):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    permission_required = "clients.add_vehicle"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = get_object_or_404(Client, id=self.kwargs["client_id"])
        context.update(
            {
                "title": f"Novo Veículo de {client.name}",
                "button_text": "Salvar",
                "cancel_url": reverse_lazy(
                    "clients:client_detail", kwargs={"pk": client.pk}
                ),
            }
        )
        return context

    def form_valid(self, form):
        client = get_object_or_404(Client, id=self.kwargs["client_id"])
        form.instance.client = client
        messages.success(self.request, "Veículo criado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao criar veículo")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "clients:client_detail", kwargs={"pk": self.kwargs["client_id"]}
        )


class UpdateClientView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView,
):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    permission_required = "clients.change_client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.object  # type: ignore
        context.update(
            {
                "title": "Editar Cliente",
                "button_text": "Atualizar",
                "cancel_url": reverse_lazy(
                    "clients:client_detail", kwargs={"pk": client.id}
                ),
            }
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Cliente atualizado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar cliente.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("clients:client_detail", kwargs={"pk": self.object.id})  # type: ignore


class UpdateVehicleView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView,
):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    permission_required = "clients.change_vehicle"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.object  # type: ignore
        context.update(
            {
                "title": "Editar Veículo",
                "button_text": "Atualizar",
                "cancel_url": reverse_lazy(
                    "clients:client_detail", kwargs={"pk": vehicle.client.id}
                ),
            }
        )
        return context

    def form_valid(self, form):
        messages.success(self.request, "Veículo atualizado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar veículo")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            "clients:client_detail", kwargs={"pk": self.object.client.pk}  # type: ignore
        )


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "clients.change_client"

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)

        client.soft_delete()

        messages.success(
            request,
            f"Cliente {client.name} removido com sucesso.",
        )

        return redirect("clients:clients_list")


class VehicleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "clients.change_vehicle"

    def post(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        client_id = vehicle.client.pk

        vehicle.soft_delete()

        messages.success(
            request,
            f"Veículo {vehicle.vehicle_model} removido com sucesso.",
        )

        return redirect("clients:client_detail", pk=client_id)
