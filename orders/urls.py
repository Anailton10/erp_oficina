from django.urls import path

from . import views

urlpatterns = [
    path('list/orders/', views.OrderListView.as_view(), name='order_list'),
    path('list/orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('create/<int:client_id>/<int:vehicle_id>/',views.OrderCreateView.as_view(),name='create_order'),
    path("add-item-modal/<int:order_id>/", views.AddOrderItemModalView.as_view(), name="add_item_modal"),
    path("<int:order_id>/add-item/", views.AddOrderItemView.as_view(), name="add_item"),
]