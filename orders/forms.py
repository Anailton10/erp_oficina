from django import forms

from products.models import CatalogItem

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Não inclui 'client' e 'vehicle', vê da view para setar esses campos
        fields = ['status', 'description']


class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=CatalogItem.objects.all().order_by('type', 'name'),
        required=True,
        label='Produto / Serviço',
        empty_label='Selecione...',
    )

    class Meta:
        model = OrderItem
<<<<<<< Updated upstream
        fields = ['order', 'quantity', 'unit_price']
=======
        fields = ['product', 'quantity', 'unit_price']
>>>>>>> Stashed changes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({
            'class': 'form-select catalog-select',
            'onchange': 'onCatalogChange(this)',
        })
        self.fields['quantity'].widget.attrs.update({'class': 'form-control qty-input', 'min': '1'})
        self.fields['unit_price'].widget.attrs.update({'class': 'form-control price-input', 'step': '0.01', 'min': '0'})