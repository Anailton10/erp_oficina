from django.db import transaction

from .models import OrderItem


class OrderService:
    @staticmethod
    @transaction.atomic
    def add_item(order, item_product, quantity: int):
        if order.status == "done":
            raise ValueError("Não pode adicionar item após ordem finalizada")
        if item_product.has_stock_control():
            if quantity > item_product.stock:
                raise ValueError(
                    f"Estoque insificiente, estoque atual: {item_product.stock}"
                )
            item_product.stock -= quantity
            item_product.save()
        OrderItem.objects.create(
            order=order,
            product=item_product,
            quantity=quantity,
            unit_price=item_product.price,
        )

    @staticmethod
    @transaction.atomic
    def update_item(order_item, new_quantity, old_quantity):
        if order_item.order.status == "progress" or order_item.order.status == "done":
            raise ValueError("Não pode atualizar item após ordem inciada/finalizada")
        if new_quantity <= 0:
            raise ValueError("Quantidade deve ser maior que zero")

        difference = new_quantity - old_quantity
        product = order_item.product

        if product.has_stock_control():
            if difference > 0:  # Tira do estoque
                if difference > product.stock:
                    raise ValueError(
                        f"Estoque insificiente, estoque atual: {product.stock}"
                    )
                product.stock -= difference
            elif difference < 0:  # Adiciona do estoque
                product.stock += abs(difference)
            product.save()
        order_item.quantity = new_quantity
        order_item.save()

    @staticmethod
    @transaction.atomic
    def remove_item(order, order_item):
        if order.status == "progress" or order.status == "done":
            raise ValueError("Não pode remover item após ordem inciada/finalizada")
        order_item.product.stock += order_item.quantity
        order_item.product.save()
        order_item.delete()
