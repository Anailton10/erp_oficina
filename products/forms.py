from django import forms

from .models import CatalogItem


class CatalogItemForm(forms.ModelForm):
    class Meta:
        model = CatalogItem
        fields = ["name", "description", "price", "stock", "type"]

    type_filter = forms.ChoiceField(
        choices=[("", "Todos"), ("PRODUTO", "Produto"), ("SERVICO", "Serviço")],
        required=False,
        initial="",
        widget=forms.Select(
            attrs={
                "class": "form-select bg-dark text-light border-secondary",
                "onchange": "this.form.submit()",
            }
        ),
    )

    price_filter = forms.DecimalField(
        required=False,
        label="Preço",
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "placeholder": "Ex: 100.00",
                "step": "0.01",
            }
        ),
    )
