from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('list/products/', views.ProductListView.as_view(), name='product_list'),
]