from django.utils import timezone
from django.utils.formats import number_format

from clients.models import Client
from orders.models import Order
from products.models import CatalogItem


def get_status_orders():
    now = timezone.now()
    orders = Order.objects.all()
    order_status_open = orders.filter(status="open").count()
    order_status_progress = orders.filter(status="progress").count()
    order_status_done_month = orders.filter(
        status="done", order_date__year=now.year, order_date__month=now.month
    ).count()
    return dict(
        open=order_status_open,
        progress=order_status_progress,
        done=order_status_done_month,
    )


def get_sales_month():
    now = timezone.now()
    sales_month = Order.objects.filter(status="done", order_date__month=now.month)
    sales_total = sum(order.total for order in sales_month)
    return dict(total=number_format(sales_total, decimal_pos=2, force_grouping=True))


def get_number_new_clients():
    now = timezone.now()
    clients = Client.objects.filter(
        created_at__year=now.year, created_at__month=now.month
    ).count()
    return dict(client=clients)


def get_low_stock_products():
    products_low = CatalogItem.objects.filter(stock__lte=10)
    x = [{"name": product.name, "stock": product.stock} for product in products_low]
    return dict(stock_low=x)
