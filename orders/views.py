from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View,generic

from clients.models import Client, Vehicle

from .models import Order
from .forms import OrderForm, OrderItemFormSet


class OrderCreateView(View):
    def get(self, request, client_id, vehicle_id):
        client = get_object_or_404(Client, id=client_id) # Substitua pelo ID do cliente desejado
        vehicle = get_object_or_404(Vehicle, id=vehicle_id) # Substitua pelo ID do veículo desejado

        if vehicle.client != client:
            raise Http404("Veículo não pertence ao cliente")

        form = OrderForm()
        formset = OrderItemFormSet()

        context = {
        'form': form,
        'formset': formset,
        'client': client,
        'vehicle': vehicle
        }
        return render(request, 'orders/order_form.html', context)
    
    def post(self, request, client_id, vehicle_id):

        client = get_object_or_404(Client, id=client_id)
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():

            order = form.save(commit=False)
            order.client = client
            order.vehicle = vehicle
            order.save()

            formset.instance = order
            formset.save()

            return redirect('order_detail', pk=order.pk)
        context = {
            'form': form,
            'formset': formset,
            'client': client,
            'vehicle': vehicle
        }

        return render(request, 'orders/order_form.html', context)

class OrderListView(generic.ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'