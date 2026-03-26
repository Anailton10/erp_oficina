import json

from django.http import JsonResponse
from django.views import View

from products.models import CatalogItem

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
