import json

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from products.models import CatalogItem

from ..forms import OrderItemEditForm
from ..models import Order, OrderItem
from ..service import OrderService as service


class AddOrderItemView(View):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            data = json.loads(request.body)
            product = CatalogItem.objects.get(id=data["product_id"])
            service.add_item(order, product, int(data["quantity"]))
            return JsonResponse({"success": True})
        except (Order.DoesNotExist, CatalogItem.DoesNotExist):
            return JsonResponse({"error": "Recurso não encontrado"}, status=404)

        except ValueError:
            return JsonResponse({"error": "Operação inválida"}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


class DeleteOrderItemView(View):
    def post(self, request, item_id):
        try:
            item_order = get_object_or_404(OrderItem, pk=item_id)
            order_id = item_order.order.pk
            order = item_order.order
            service.remove_item(order, item_order)
            messages.success(request, "Item deletado com sucesso.")
        except ValueError as e:
            messages.error(request, f"Operação inválida, {e}")
        return redirect("orders:order_detail", pk=order_id)


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
        try:
            item = get_object_or_404(OrderItem, pk=item_id)
            order = item.order
            form = OrderItemEditForm(request.POST, instance=item)
            old_quantity = item.quantity

            if form.is_valid():
                service.update_item(
                    order_item=item,
                    new_quantity=form.cleaned_data["quantity"],
                    old_quantity=old_quantity,
                )
                order = Order.objects.prefetch_related("items__product").get(
                    pk=item.order.pk
                )
                response = render(
                    request, "orders/partials/_order_items.html", {"order": order}
                )
                response["HX-Trigger"] = "itemAdded"
                return response

            return render(
                request,
                "orders/partials/_edit_item_modal.html",
                {"form": form, "item": item},
            )
        except Exception as e:
            messages.error(request, f"Operação inválida, {e}")
            url = reverse_lazy("orders:order_detail", kwargs={"pk": order.pk})
            response = HttpResponse()
            response["HX-Redirect"] = url
            return response
