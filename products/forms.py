from django import forms

from .models import CatalogItem


class CatalogItemForm(forms.ModelForm):
    name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(
            attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "placeholder": "Nome do produto ou serviço",
            }
        ),
    )
    description = forms.CharField(
        label="Descrição",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "placeholder": "Descrição (opcional)",
                "rows": 3,
            }
        ),
    )
    price = forms.DecimalField(
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
    stock = forms.IntegerField(
        label="Estoque",
        required=False,  # <--- deixa opcional
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control bg-dark text-light border-secondary",
                "placeholder": "Quantidade em estoque",
            }
        ),
    )
    type = forms.ChoiceField(
        choices=[("PRODUTO", "Produto"), ("SERVICO", "Serviço")],
        label="Tipo",
        widget=forms.Select(
            attrs={
                "class": "form-select bg-dark text-light border-secondary",
            }
        ),
    )

    # Filtros extras
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

    class Meta:
        model = CatalogItem
        fields = ["name", "description", "price", "stock", "type"]

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        item_type = self.cleaned_data.get("type")
        if item_type == "PRODUTO" and (stock is None or stock < 0):
            raise forms.ValidationError("Produto precisa de estoque válido")
        return stock
