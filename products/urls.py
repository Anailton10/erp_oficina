from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("list/products/", views.ProductListView.as_view(), name="list"),
    path("detail/products/<int:pk>", views.ProductDetailView.as_view(), name="detail"),
    path("create/products/", views.ProductCreateView.as_view(), name="create"),
    path("update/products/<int:pk>", views.ProductUpdatedView.as_view(), name="update"),
    path("delete/products/<int:pk>", views.ProductDeleteView.as_view(), name="delete"),
]
