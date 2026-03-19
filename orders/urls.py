from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('list/orders/', views.OrderListView.as_view(), name='order_list'),
    path('create/<int:client_id>/<int:vehicle_id>/',views.OrderCreateView.as_view(),name='create_order'),
]