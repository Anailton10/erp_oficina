from django import forms

from products.models import CatalogItem

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status", "description"]
        labels = {
            "status": "Status da ordem",
            "description": "Observações",
        }
        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-select bg-dark text-light border-secondary"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control bg-dark text-light border-secondary",
                    "rows": 3,
                    "placeholder": "Descreva o serviço ou observações da ordem...",
                }
            ),
        }


class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=CatalogItem.objects.all().order_by("type", "name"),
        required=True,
        label="Item",
        empty_label="Selecione um produto ou serviço",
    )

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "unit_price"]
        labels = {
            "quantity": "Quantidade",
            "unit_price": "Preço unitário (R$)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["product"].widget.attrs.update({
            "class": "form-select catalog-select bg-dark text-light border-secondary",
            "onchange": "onCatalogChange(this)",
        })

        self.fields["quantity"].widget.attrs.update({
            "class": "form-control qty-input bg-dark text-light border-secondary",
            "min": "1",
            "placeholder": "Qtd",
        })

        self.fields["unit_price"].widget.attrs.update({
            "class": "form-control price-input bg-dark text-light border-secondary",
            "step": "0.01",
            "min": "0",
            "placeholder": "0.00",
        })


class OrderItemEditForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["quantity", "unit_price"]
        labels = {
            "quantity": "Quantidade",
            "unit_price": "Preço unitário (R$)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["quantity"].widget.attrs.update({
            "class": "form-control qty-input bg-dark text-light border-secondary",
            "min": "1",
        })

        self.fields["unit_price"].widget.attrs.update({
            "class": "form-control price-input bg-dark text-light border-secondary",
            "step": "0.01",
            "min": "0",
        })
