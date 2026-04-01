from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import CatalogItemForm
from .models import CatalogItem


class ProductListView(generic.ListView):
    model = CatalogItem
    template_name = "products/product_list.html"
    paginate_by = 8
    context_object_name = "items"

    def get_queryset(self):
        queryset = super().get_queryset()
        products_is_active = self.request.GET.get("active")
        product_type = self.request.GET.get("type_filter")
        product_name = self.request.GET.get("name")
        product_price = self.request.GET.get("price_filter")

        if products_is_active == "false":
            queryset = queryset.filter(is_active=False)
        else:
            queryset = queryset.filter(is_active=True)

        if product_type:
            queryset = queryset.filter(type=product_type)

        if product_name:
            queryset = queryset.filter(name__icontains=product_name)

        if product_price:
            queryset = queryset.filter(price__lte=product_price)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filter_form"] = CatalogItemForm(self.request.GET or None)
        return context


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

    def form_valid(self, form):
        if form.cleaned_data["type"] == "produto":
            messages.success(self.request, "Produto criado com sucesso.")
        messages.success(self.request, "Serviço criado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao criar produto.")
        return super().form_invalid(form)

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

    def form_valid(self, form):
        messages.success(self.request, "Produto atualizado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar produto.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("products:detail", kwargs={"pk": self.kwargs["pk"]})


class ProductDeleteView(View):
    def post(self, request, pk):
        product = get_object_or_404(CatalogItem, pk=pk)  # noqa: F811

        product.soft_delete()

        messages.success(
            request,
            f"Produto/Serviço {product.name} removido com sucesso.",
        )

        return redirect("products:list")
