from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from . import metrics


class Home(LoginRequiredMixin, TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_metrics_status = metrics.get_status_orders()
        new_clients = metrics.get_number_new_clients()
        products_low = metrics.get_low_stock_products()
        sales = metrics.get_sales_month()
        owner = self.request.user.groups.filter(name="Owner").exists()
        context["orders_open"] = order_metrics_status["open"]
        context["orders_progress"] = order_metrics_status["progress"]
        context["orders_done_month"] = order_metrics_status["done"]
        context["clients_month"] = new_clients["client"]
        context["products_low"] = products_low["stock_low"]
        context["owner"] = owner
        context["sales"] = sales["total"]

        return context
