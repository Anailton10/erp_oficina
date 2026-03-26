from django.urls import path

from orders.views import order_item_views, order_views

app_name = "orders"

urlpatterns = [
    path("list/orders/", order_views.OrderListView.as_view(), name="order_list"),
    path(
        "list/orders/<int:pk>/",
        order_views.OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "create/<int:client_id>/<int:vehicle_id>/",
        order_views.OrderCreateView.as_view(),
        name="create_order",
    ),
    path(
        "update/<int:order_id>/",
        order_views.OrderUpdateView.as_view(),
        name="update_status",
    ),
    path(
        "<int:order_id>/add-item/",
        order_item_views.AddOrderItemView.as_view(),
        name="add_item",
    ),
    path(
        "<int:item_id>/delete-item/",
        order_item_views.DeleteOrderItemView.as_view(),
        name="delete_item",
    ),
    path(
        "<int:item_id>/update-item/",
        order_item_views.UpdateOrderItemView.as_view(),
        name="update_item",
    ),
]
