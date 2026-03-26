from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View, generic

from clients.models import Client, Vehicle
from products.models import CatalogItem

from ..forms import OrderForm
from ..models import Order


class OrderCreateView(View):
    def get(self, request, client_id, vehicle_id):
        client = get_object_or_404(Client, id=client_id)
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        if vehicle.client != client:
            raise Http404("Veículo não pertence ao cliente")
        form = OrderForm()
        return render(
            request,
            "orders/order_form.html",
            {
                "form": form,
                "client": client,
                "vehicle": vehicle,
            },
        )

    def post(self, request, client_id, vehicle_id):
        client = get_object_or_404(Client, id=client_id)
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = client
            order.vehicle = vehicle
            order.save()
            return redirect("orders:order_detail", pk=order.pk)
        return render(
            request,
            "orders/order_form.html",
            {
                "form": form,
                "client": client,
                "vehicle": vehicle,
            },
        )


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["catalog_items"] = CatalogItem.objects.all().order_by("type", "name")
        return context
