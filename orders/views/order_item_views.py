from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from products.models import CatalogItem

from ..forms import OrderItemEditForm
from ..models import Order, OrderItem
from ..service import OrderService as service


class AddOrderItemView(View):
    def get(self, request):
        products = CatalogItem.objects.all()
        name = request.GET.get("name", "")
        type = request.GET.get("type", "")

        if name:
            products = products.filter(name__icontains=name)
        if type:
            products = products.filter(type=type)

        return render(
            request,
            "orders/partials/_catalog_items.html",
            {
                "products": products,
            },
        )

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            product = CatalogItem.objects.get(id=request.POST["product_id"])
            service.add_item(order, product, int(request.POST["quantity"]))

            return render(
                request, "orders/partials/_order_items.html", {"order": order}
            )

        except (Order.DoesNotExist, CatalogItem.DoesNotExist):

            return HttpResponse("Recurso não encontrado", status=404)
        except ValueError as e:
            return HttpResponse(str(e), status=400)
        except Exception as e:
            return HttpResponse(str(e), status=500)


class DeleteOrderItemView(View):
    def post(self, request, item_id):
        item_order = get_object_or_404(OrderItem, pk=item_id)
        order = item_order.order

        try:
            service.remove_item(order, item_order)
            messages.success(request, "Item deletado com sucesso.")
        except ValueError as e:
            messages.error(request, f"Operação inválida: {e}")

        return redirect("orders:order_detail", pk=order.pk)


class UpdateOrderItemView(View):
    def get(self, request, item_id):
        item = get_object_or_404(OrderItem, pk=item_id)
        form = OrderItemEditForm(instance=item)
        return render(
            request,
            "orders/partials/_edit_item_modal.html",
            {"form": form, "item": item},
        )

    def post(self, request, item_id):
        item = get_object_or_404(OrderItem, pk=item_id)
        order = item.order
        form = OrderItemEditForm(request.POST, instance=item)
        try:
            old_quantity = item.quantity
            if form.is_valid():
                service.update_item(
                    order_item=item,
                    new_quantity=form.cleaned_data["quantity"],
                    old_quantity=old_quantity,
                )
                return render(
                    request,
                    "orders/partials/_order_items.html",
                    {"order": order},
                )
            return render(
                request,
                "orders/partials/_edit_item_modal.html",
                {"form": form, "item": item},
            )
        except Exception as e:
            return HttpResponse(str(e), status=400)
