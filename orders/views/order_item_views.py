import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from products.models import CatalogItem

from ..forms import OrderItemEditForm
from ..models import Order, OrderItem


class AddOrderItemView(View):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            data = json.loads(request.body)
            product = CatalogItem.objects.get(id=data["product_id"])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=int(data["quantity"]),
                unit_price=data["unit_price"],
            )
            return JsonResponse({"success": True})
        # TODO: Tratar melhor os possiveis erros ""Order.DoesNotExist, CatalogItem.DoesNotExist"
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


class DeleteOrderItemView(View):
    def post(self, request, item_id):
        item = get_object_or_404(OrderItem, pk=item_id)
        order_id = item.order.pk
        item.delete()
        messages.success(request, "Item deletado com sucesso.")

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
            print(form.errors)
            if form.is_valid():
                form.save()
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
            return JsonResponse({"success": False, "error": str(e)})
