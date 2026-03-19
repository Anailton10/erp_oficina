# from django.shortcuts import render
from django.views import generic
from .models import CatalogItem


class ProductListView(generic.ListView):
    model = CatalogItem
    template_name = 'products/product_list.html'
    context_object_name = 'items'