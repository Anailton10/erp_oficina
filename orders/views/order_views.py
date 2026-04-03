import datetime as dt

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views import View, generic
from weasyprint import HTML

from clients.models import Client, Vehicle
from products.models import CatalogItem

from ..forms import OrderForm
from ..models import Order


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Order
    template_name = "orders/order_list.html"
    paginate_by = 10
    context_object_name = "orders"
    permission_required = "orders.view_order"

    def get_queryset(self):
        return Order.objects.filter(is_active=True)


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"
    permission_required = "orders.view_order"

    def get_queryset(self):
        return Order.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["catalog_items"] = CatalogItem.objects.filter(is_active=True).order_by(
            "type", "name"
        )
        return context


class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "orders.add_order"

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

        if vehicle.client != client:
            raise Http404("Veículo não pertence ao cliente")

        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.client = client
            order.vehicle = vehicle
            order.save()

            messages.success(request, "Ordem criada com sucesso.")
            return redirect("orders:order_detail", pk=order.pk)

        messages.error(request, "Erro ao criar ordem.")
        return render(
            request,
            "orders/order_form.html",
            {
                "form": form,
                "client": client,
                "vehicle": vehicle,
            },
        )


class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "orders.change_order"

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        try:
            order.transition_status()
            messages.success(request, "Status atualizado com sucesso.")
        except ValueError as e:
            messages.error(request, f"Operação inválida: {e}")

        return redirect("orders:order_detail", pk=order_id)


class OrderDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "orders.delete_order"

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order_number = order.number

        order.soft_delete()

        messages.success(request, f"Ordem {order_number} removida com sucesso.")

        return redirect("orders:order_list")


class OrderPDFView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "orders.view_order"

    def get(self, request, order_id):
        # 1. buscar a OS
        order = get_object_or_404(Order, pk=order_id)
        time_registration = dt.datetime.now().strftime("%d/%m/%y, %H:%M %p")
        print(f"TESTE HORA: {time_registration}")
        # 2. renderizar o template HTML com os dados
        html_string = render_to_string(
            "orders/partials/_order_pdf.html",
            {
                "order": order,
                "time_registration": time_registration,
            },
        )
        # 3. converter HTML pra PDF com WeasyPrint
        pdf = HTML(string=html_string).write_pdf()
        # 4. retornar o HttpResponse com o PDF
        response = HttpResponse(pdf, content_type="application/pdf")
        if request.GET.get("download") == "true":
            response["Content-Disposition"] = (
                f'attachment; filename="os_{order.number}.pdf"'
            )
        else:
            response["Content-Disposition"] = (
                f'inline; filename="os_{order.number}.pdf"'
            )

        return response
