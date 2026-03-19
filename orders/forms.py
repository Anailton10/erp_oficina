from django import forms

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Não inclui 'client' e 'vehicle', vê da view para setar esses campos
        fields = ['status', 'description']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'order', 'quantity', 'unit_price', ]


# Cria um formset para os itens do pedido, permitindo adicionar múltiplos itens em um único formulário de pedido
OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm, 
    extra=1,
    can_delete=True
)