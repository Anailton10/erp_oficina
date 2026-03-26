from ast import arg

from django.db import models

from clients.models import Client, Vehicle
from products.models import CatalogItem


class Order(models.Model):
    STATUS_CHOICES = [
        ("open", "Aberto"),
        ("progress", "Em Progresso"),
        ("done", "Finalizado"),
    ]
    number = models.CharField(max_length=20, unique=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="open")
    description = models.TextField(blank=True, null=True)

    @property
    def total(self):
        # Calcula o total do pedido somando o preço de cada item multiplicado pela quantidade
        return sum(item.quantity * item.unit_price for item in self.items.all())

    def save(self, *args, **kwargs):

        if not self.number:
            last_order = Order.objects.order_by("-id").first()

            if last_order and last_order.number:
                last_number = int(last_order.number.split("-")[1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.number = f"OS-{new_number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.number} - {self.client.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        CatalogItem, on_delete=models.PROTECT, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.unit_price

    # Sobrescreve o método save para definir o preço unitário com base no produto selecionado, se não for fornecido
    def save(self, *args, **kwargs):
        if self.product and not self.unit_price:
            self.unit_price = self.product.price

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.product.price}"
