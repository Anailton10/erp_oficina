from django import forms
from .models import CatalogItem

class CatalogItemForm(forms.ModelForm):
    class Meta:
        model = CatalogItem
        fields = ['name', 'description', 'price', 'stock', 'type']