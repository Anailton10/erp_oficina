from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import CatalogItemForm
from .models import CatalogItem


class ProductListView(generic.ListView):
    model = CatalogItem
    template_name = "products/product_list.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = CatalogItem.objects.all()

        products_is_active = self.request.GET.get("active")

        if products_is_active == "false":
            queryset = queryset.filter(is_active=False)
        else:
            queryset = queryset.filter(is_active=True)

        return queryset


class ProductDetailView(generic.DetailView):
    model = CatalogItem
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ProductCreateView(generic.CreateView):
    model = CatalogItem
    template_name = "products/product_form.html"
    form_class = CatalogItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "title": "Novo Produto",
                "button_text": "Salvar",
                "cancel_url": reverse_lazy("products:list"),
            }
        )
        return context

    def get_success_url(self):
        return reverse_lazy("products:list")


class ProductUpdatedView(generic.UpdateView):
    model = CatalogItem
    template_name = "products/product_form.html"
    form_class = CatalogItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "title": "Editar Produto",
                "button_text": "Atualizar",
                "cancel_url": reverse_lazy(
                    "products:detail", kwargs={"pk": self.kwargs["pk"]}
                ),
            }
        )
        return context

    def get_success_url(self):
        return reverse_lazy("products:detail", kwargs={"pk": self.kwargs["pk"]})


class ProductDeleteView(View):
    def post(self, request, pk):
        product = get_object_or_404(CatalogItem, pk=pk)

        product.soft_delete()

        messages.success(
            request, f"Produco/Serviço {product.name} removido com sucesso"
        )
        return redirect("products:list")
